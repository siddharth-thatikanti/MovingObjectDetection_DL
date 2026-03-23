import os

label_root = "dataset/kitti/labels"
classes = set()
MAX_FILES = 200   # fast sample check

for split in ["train", "val"]:
    path = os.path.join(label_root, split)
    files = [f for f in os.listdir(path) if f.endswith(".txt")][:MAX_FILES]

    for file in files:
        with open(os.path.join(path, file), "r") as f:
            line = f.readline().strip()
            if line:
                cls = int(line.split()[0])
                classes.add(cls)

print("✅ Classes found (sampled):", sorted(classes))
