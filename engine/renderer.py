"""
engine/renderer.py

Renderer with support for:
- Single character rendering
- Multiple character rendering
- Character direction flipping
- Facial expressions
- Camera zoom
- PNG frame generation
- MP4 encoding
"""

import os
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw


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



def draw_pose(
    draw,
    pose,
    origin_x,
    origin_y,
    scale,
    line_width,
    head_radius,
    direction="right",
):

    def to_screen(name):

        x, y = pose[name]

        if direction == "left":
            x = -x

        return (
            origin_x + x * scale,
            origin_y + y * scale
        )


    for a, b in BONES:

        draw.line(
            [
                to_screen(a),
                to_screen(b)
            ],
            fill=(20, 20, 20),
            width=int(line_width)
        )


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



def draw_face(
    draw,
    character,
    pose,
    origin_x,
    origin_y,
    scale,
):
    """
    Draw simple readable facial expressions.
    """

    expression = character.get_expression()


    head_x, head_y = pose["head"]

    x = origin_x + head_x * scale
    y = origin_y + head_y * scale


    eye_y = y - 3 * scale
    eye_offset = 5 * scale

    eye_size = max(
        1,
        int(scale * 2)
    )


    # Eyes

    if expression == "angry":

        draw.line(
            [
                (x - eye_offset, eye_y - 2),
                (x - eye_offset + 5, eye_y + 2)
            ],
            fill=(20,20,20),
            width=2
        )

        draw.line(
            [
                (x + eye_offset - 5, eye_y + 2),
                (x + eye_offset, eye_y - 2)
            ],
            fill=(20,20,20),
            width=2
        )


    elif expression == "surprised":

        draw.ellipse(
            [
                x - eye_offset - eye_size,
                eye_y - eye_size,
                x - eye_offset + eye_size,
                eye_y + eye_size
            ],
            outline=(20,20,20),
            width=1
        )

        draw.ellipse(
            [
                x + eye_offset - eye_size,
                eye_y - eye_size,
                x + eye_offset + eye_size,
                eye_y + eye_size
            ],
            outline=(20,20,20),
            width=1
        )


    else:

        draw.ellipse(
            [
                x - eye_offset - eye_size,
                eye_y - eye_size,
                x - eye_offset + eye_size,
                eye_y + eye_size
            ],
            fill=(20,20,20)
        )

        draw.ellipse(
            [
                x + eye_offset - eye_size,
                eye_y - eye_size,
                x + eye_offset + eye_size,
                eye_y + eye_size
            ],
            fill=(20,20,20)
        )


    # Mouth

    mouth_y = y + 8 * scale


    if expression == "happy":

        draw.arc(
            [
                x - 8 * scale,
                mouth_y - 4 * scale,
                x + 8 * scale,
                mouth_y + 8 * scale
            ],
            0,
            180,
            fill=(20,20,20),
            width=2
        )


    elif expression == "sad":

        draw.arc(
            [
                x - 8 * scale,
                mouth_y,
                x + 8 * scale,
                mouth_y + 10 * scale
            ],
            180,
            360,
            fill=(20,20,20),
            width=2
        )


    elif expression == "surprised":

        draw.ellipse(
            [
                x - 4 * scale,
                mouth_y - 2 * scale,
                x + 4 * scale,
                mouth_y + 8 * scale
            ],
            outline=(20,20,20),
            width=2
        )


    else:

        draw.line(
            [
                (x - 6 * scale, mouth_y),
                (x + 6 * scale, mouth_y)
            ],
            fill=(20,20,20),
            width=2
        )



def draw_characters(
    draw,
    characters,
    poses,
    figure_scale
):

    for character, pose in zip(characters, poses):

        x = character.position[0]
        y = character.position[1]

        scale = figure_scale * character.scale


        draw_pose(
            draw,
            pose,
            x,
            y,
            scale,
            3,
            13,
            character.direction
        )


        draw_face(
            draw,
            character,
            pose,
            x,
            y,
            scale
        )



def render_scene(
    compose_frame_fn,
    output_path,
    duration,
    width=960,
    height=540,
    fps=30,
    background_color=(255,255,255),
    walk_x_fn=None,
    zoom_start=1.0,
    zoom_end=1.0,
    zoom_top_bias=0.35,
):

    temp_dir = os.path.join(
        os.path.dirname(os.path.abspath(output_path)),
        "_renderer_frames_tmp"
    )


    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


    os.makedirs(temp_dir)


    total_frames = int(duration * fps)

    ground_y = height * 0.72
    figure_scale = height / 420.0



    for frame in range(total_frames):

        progress = frame / max(1,total_frames-1)

        time = frame / fps


        img = Image.new(
            "RGB",
            (width,height),
            background_color
        )


        draw = ImageDraw.Draw(img)


        draw.line(
            [
                (0,ground_y),
                (width,ground_y)
            ],
            fill=(210,210,210),
            width=2
        )


        frame_data = compose_frame_fn(time)


        if (
            isinstance(frame_data,dict)
            and "characters" in frame_data
            and "poses" in frame_data
        ):

            draw_characters(
                draw,
                frame_data["characters"],
                frame_data["poses"],
                figure_scale
            )


        else:

            pose = frame_data

            direction = "right"


            if isinstance(frame_data,dict):

                pose = frame_data.get(
                    "pose",
                    frame_data
                )

                direction = frame_data.get(
                    "direction",
                    "right"
                )


            origin_x = (
                walk_x_fn(time)
                if walk_x_fn
                else width/2
            )


            draw_pose(
                draw,
                pose,
                origin_x,
                ground_y,
                figure_scale,
                3,
                13,
                direction
            )


        zoom = lerp(
            zoom_start,
            zoom_end,
            progress
        )


        if zoom > 1.001:

            zoom_width = int(width * zoom)
            zoom_height = int(height * zoom)


            enlarged = img.resize(
                (zoom_width,zoom_height),
                Image.Resampling.BILINEAR
            )


            left = (zoom_width-width)//2

            top = int(
                (zoom_height-height)
                * zoom_top_bias
            )


            img = enlarged.crop(
                (
                    left,
                    top,
                    left+width,
                    top+height
                )
            )


        img.save(
            os.path.join(
                temp_dir,
                f"frame_{frame:06d}.png"
            )
        )



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