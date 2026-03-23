def load_temporal_frames(frames, index):
    prev = frames[max(index-1, 0)]
    curr = frames[index]
    next = frames[min(index+1, len(frames)-1)]
    return prev, curr, next
