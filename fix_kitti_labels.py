import os

CLASS_MAP = {
    0: 0,  # Car
    3: 1,  # Pedestrian
    5: 2   # Cyclist
}

def clean_labels(label_dir):
    removed = 0

    for file in os.listdir(label_dir):
        if not file.endswith(".txt"):
            continue

        path = os.path.join(label_dir, file)
        valid_lines = []

        with open(path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue

                cls = int(parts[0])
                if cls in CLASS_MAP:
                    parts[0] = str(CLASS_MAP[cls])
                    valid_lines.append(" ".join(parts))

        if valid_lines:
            with open(path, "w") as f:
                f.write("\n".join(valid_lines))
        else:
            os.remove(path)
            removed += 1

    print(f"✔ Cleaned {label_dir}, removed {removed} empty label files")

clean_labels("dataset/kitti/labels/train")
clean_labels("dataset/kitti/labels/val")
