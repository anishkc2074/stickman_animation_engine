from library.background_library import background_library

print("All Backgrounds")
print("----------------")

for bg in background_library.all():
    print(f"Name: {bg.name}")
    print(f"Category: {bg.category}")
    print(f"Image: {bg.image_path}")
    print(f"Ground Y: {bg.ground_y}")
    print(f"Tags: {bg.tags}")
    print()

print("Search Result")
print("----------------")

results = background_library.search("forest")

for bg in results:
    print(bg.name)