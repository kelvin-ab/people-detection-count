def get_blob_shape(layer, batch_size: int):
    shape = layer.shape.copy()
    layout = layer.layout

    try:
        batch_index = layout.index('N')
    except ValueError:
        batch_index = 1 if layout == 'C' else -1

    if batch_index != -1 and shape[batch_index] != batch_size:
        shape[batch_index] = batch_size

    return shape