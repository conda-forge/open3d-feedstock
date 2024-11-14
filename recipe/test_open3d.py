import traceback

try:
    import open3d
    print('Open3D imported successfully')
except Exception as e:
    print(f'Failed to import Open3D. Error: {e}')
    traceback.print_exc()
