"""
engine/renderer.py

Milestone 1:
Basic frame renderer.

Responsibilities:
- Create blank frames
- Draw a simple stickman pose
- Add ground line
- Apply simple camera zoom
- Save PNG frames
- Encode frames into MP4 using ffmpeg

No animation system exists yet.
The renderer only receives a pose function from outside.
"""

import os
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw


# Simple skeleton connections
BONES = [
    ("pelvis", "chest"),
    ("chest", "neck"),
    ("neck", "head"),

    ("chest", "l_shoulder"),
    ("l_shoulder", "l_elbow"),
    ("l_elbow", "l_hand"),

    ("chest", "r_shoulder"),
    ("r_shoulder", "r_elbow"),
    ("r_elbow", "r_hand"),

    ("pelvis", "l_hip"),
    ("l_hip", "l_knee"),
    ("l_knee", "l_foot"),

    ("pelvis", "r_hip"),
    ("r_hip", "r_knee"),
    ("r_knee", "r_foot"),
]


def lerp(a, b, t):
    return a + (b - a) * t


def draw_pose(draw, pose, origin_x, origin_y, scale, line_width, head_radius):

    def to_screen(name):
        x, y = pose[name]
        return (
            origin_x + x * scale,
            origin_y + y * scale
        )

    # Draw body bones
    for a, b in BONES:
        draw.line(
            [
                to_screen(a),
                to_screen(b)
            ],
            fill=(20, 20, 20),
            width=int(line_width)
        )

    # Draw head
    hx, hy = to_screen("head")

    r = head_radius * scale

    draw.ellipse(
        [
            hx - r,
            hy - r,
            hx + r,
            hy + r
        ],
        fill=(255, 255, 255),
        outline=(20, 20, 20),
        width=int(line_width * 0.7)
    )


def render_scene(
    compose_frame_fn,
    output_path,
    duration,
    width=960,
    height=540,
    fps=30,
    background_color=(255, 255, 255),
    walk_x_fn=None,
    zoom_start=1.0,
    zoom_end=1.0,
    zoom_top_bias=0.35,
):
    """
    Render animation.

    compose_frame_fn(t)
        Returns stickman pose at time t.

    output_path
        Final mp4 file location.
    """

    temp_dir = os.path.join(
        os.path.dirname(os.path.abspath(output_path)) or ".",
        "_renderer_frames_tmp"
    )

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    os.makedirs(temp_dir, exist_ok=True)


    total_frames = int(round(duration * fps))

    ground_y = height * 0.72

    figure_scale = height / 420.0


    for frame in range(total_frames):

        progress = frame / max(1, total_frames - 1)

        time = frame / fps


        img = Image.new(
            "RGB",
            (width, height),
            background_color
        )

        draw = ImageDraw.Draw(img)


        # Ground
        draw.line(
            [
                (0, ground_y),
                (width, ground_y)
            ],
            fill=(210, 210, 210),
            width=2
        )


        # Character position
        if walk_x_fn:
            origin_x = walk_x_fn(time)
        else:
            origin_x = width / 2


        pose = compose_frame_fn(time)


        draw_pose(
            draw,
            pose,
            origin_x,
            ground_y,
            figure_scale,
            max(3, height * 0.014),
            13
        )


        # Camera zoom
        zoom = lerp(
            zoom_start,
            zoom_end,
            progress
        )


        if zoom > 1.001:

            zoom_width = int(width * zoom)
            zoom_height = int(height * zoom)


            enlarged = img.resize(
                (zoom_width, zoom_height),
                Image.BILINEAR
            )


            left = (zoom_width - width) // 2

            top = int(
                (zoom_height - height)
                * zoom_top_bias
            )


            img = enlarged.crop(
                (
                    left,
                    top,
                    left + width,
                    top + height
                )
            )


        img.save(
            os.path.join(
                temp_dir,
                f"frame_{frame:06d}.png"
            )
        )


    # Encode video
    command = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(fps),
        "-i",
        os.path.join(
            temp_dir,
            "frame_%06d.png"
        ),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        output_path
    ]


    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )


    if result.returncode != 0:
        print(
            result.stderr,
            file=sys.stderr
        )
        raise RuntimeError(
            "ffmpeg encoding failed"
        )


    shutil.rmtree(temp_dir)

    return output_path