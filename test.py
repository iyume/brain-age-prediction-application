from pathlib import Path

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np

from brain_age_prediction.evaluate import Evaluator
from brain_age_prediction.trainer import Trainer

# trainer = Trainer(device="cuda")
# trainer.train()

# # each epoch mae
# mae_errors = []
# for i in range(1, 101):
#     evaluator = Evaluator("cuda", pth_file=f"ckpt/model_v1_epoch{i}.pth")
#     mae = evaluator.test()
#     mae_errors.append(mae)
# print(mae_errors)


# data = nib.load("datasets/IXI/IXI002-Guys-0828-T1.nii").get_fdata()

# fig, axes = plt.subplots(1, 3)
# axes = axes.flatten()
# for ax in axes:
#     ax.axis("off")
# axes[0].imshow(data[:, :, data.shape[2] // 2], cmap="gray")
# axes[1].imshow(data[:, data.shape[1] // 2, :], cmap="gray")
# axes[2].imshow(data[data.shape[0] // 2, :, :], cmap="gray")
# axes[0].imshow(data[:, :, data.shape[2] // 5], cmap="gray")
# axes[1].imshow(data[:, :, data.shape[2] * 2 // 5], cmap="gray")
# axes[2].imshow(data[:, :, data.shape[2] * 3 // 5], cmap="gray")
# axes[3].imshow(data[:, :, data.shape[2] * 4 // 5], cmap="gray")
# fig.savefig("output_slice.png", dpi=100, bbox_inches="tight", transparent=True)


# img = np.rot90(data[:, :, data.shape[2] // 2])
# plt.imshow(img, cmap="gray", aspect="equal")
# plt.axis("off")
# plt.savefig("output_slice.png", bbox_inches="tight", pad_inches=0)
