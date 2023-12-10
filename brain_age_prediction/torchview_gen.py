from torchview import draw_graph

from .model import BrainAgePredictionResNet

model_graph = draw_graph(
    BrainAgePredictionResNet(),
    input_size=(1, 256, 256, 128),
    graph_name="BrainAgePredictionResNet-depth3",
    depth=3,
)
model_graph.visual_graph.render(
    directory="torchview_graphs",
    view=False,
    format="png",
)

model_graph = draw_graph(
    BrainAgePredictionResNet(),
    input_size=(1, 256, 256, 128),
    graph_name="BrainAgePredictionResNet-depth2",
    depth=2,
)
model_graph.visual_graph.render(
    directory="torchview_graphs",
    view=False,
    format="png",
)

model_graph = draw_graph(
    BrainAgePredictionResNet(),
    input_size=(1, 256, 256, 128),
    graph_name="BrainAgePredictionResNet-depth1",
    depth=1,
)
model_graph.visual_graph.render(
    directory="torchview_graphs",
    view=False,
    format="png",
)
