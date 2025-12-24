from vispy import scene
from vispy.geometry import MeshData
from vispy.scene import visuals


class MainWindow(scene.SceneCanvas):
    """
    Main window for rendering 3D models using Vispy.

    This class provides a graphical interface for rendering 3D models using the Vispy library.
    It sets up a scene canvas with interactive capabilities, allowing users to visualize and
    interact with 3D models. The canvas includes a grid layout and a view with a configurable
    camera for easy manipulation of the 3D scene.

    Parameters
    ----------
    camera : str, optional
        Camera type for the view. Options are "turntable", "arcball", "fly", "panzoom".
        Default is "turntable".
    fov : float, optional
        Field of view in degrees. Only applicable for 3D cameras.
        Default is 60.
    bgcolor : str or tuple, optional
        Background color of the view. Can be a color name (e.g., "black", "white") or
        an RGBA tuple. Default is "black".
    size : tuple of int, optional
        Window size as (width, height). Default is (800, 600).
    """

    def __init__(self, camera="turntable", fov=60, bgcolor="black", size=(800, 600)):
        super().__init__(keys="interactive", size=size, show=True)
        self.unfreeze()
        self.grid = self.central_widget.add_grid(margin=10)
        self.view = self.grid.add_view(row=0, col=0, camera=camera)
        self.view.bgcolor = bgcolor
        self.view.camera.fov = fov

    def set_model(self, vertices, faces, shading="smooth", color="grey"):
        """
        Set the 3D model to be rendered.

        This method takes arrays of vertices and faces, creates a mesh from them, and adds
        the mesh to the view for rendering.

        Parameters
        ----------
        vertices : numpy.ndarray
            Array of vertex coordinates.
        faces : numpy.ndarray
            Array of face indices.
        shading : str, optional
            Shading mode for the mesh. Options are "smooth", "flat", or None.
            Default is "smooth".
        color : str or tuple, optional
            Color of the mesh. Can be a color name (e.g., "grey", "red") or
            an RGBA tuple (e.g., (1.0, 0.5, 0.5, 1.0)). Default is "grey".
        """
        mesh_data = MeshData(vertices=vertices, faces=faces)
        mesh = visuals.Mesh(meshdata=mesh_data, shading=shading, color=color)
        self.view.add(mesh)
