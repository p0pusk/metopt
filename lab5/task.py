import numpy as np

dim = 3

f = lambda x: 4 * x[0] + x[1] + 4 * np.sqrt(1 + 3 * x[0] ** 2 + x[1] ** 2) + x[2] ** 2

grad_f = lambda x: [
    4 + 12 * (x[0] / np.sqrt(1 + 3 * x[0] ** 2 + x[1] ** 2)),
    1 + 4 * (x[1] / np.sqrt(1 + 3 * x[0] ** 2 + x[1] ** 2)),
    2 * x[2]
]

rs = [
    lambda x: 7 * (x[0] + 1) ** 2 + (x[1] + 1) ** 2 + (x[2] - np.log(2)) ** 2 - 4,
    lambda x: (x[0] - 1 / 2) ** 2 + (x[1] + 1) ** 2 + (x[2] + 1) ** 2 - 4,
    lambda x: (x[0] + 2) ** 2 / 4 + 8 * (x[1] + 0.5) ** 2 + x[2] ** 2 - 2.5,
    lambda x: x[2] - 0.5,
    lambda x: 4 * x[0] + x[1] + 4 * np.sqrt(1 + 3 * x[0] ** 2 + x[1] ** 2) + x[2] ** 2 - 3.10
]

grad_rs = [
    lambda x: [14 * (x[0] + 2), 2 * (x[1] + 1), 2 * (x[2] - np.log(2))],
    lambda x: [2 * (x[0] - 0.5), 2 * (x[1] + 1), 2 * (x[2] + 1)],
    lambda x: [0.5 * (x[0] + 2), 2 * 16 * (x[1] + 0.5), 2 * x[2]],
    lambda x: [0, 0, 1]
]


# def f(x):
#     return 2 * x[0] + x[1] + x[2] / 2 + 4 * np.sqrt(5 * (x[0] ** 2) + 3 * (x[1] ** 2) + 2 * (x[2] ** 2) + 1)
#
#
# def grad_f(x):
#     return np.array([
#         2 + (10 * x[0]) / np.sqrt(5 * (x[0] ** 2) + 3 * (x[1] ** 2) + 2 * (x[2] ** 2) + 1),
#         1 + (12 * x[1]) / np.sqrt(5 * (x[0] ** 2) + 3 * (x[1] ** 2) + 2 * (x[2] ** 2) + 1),
#         1 / 2 + (8 * x[2]) / np.sqrt(5 * (x[0] ** 2) + 3 * (x[1] ** 2) + 2 * (x[2] ** 2) + 1)
#     ])
#
#
# rs = [
#     lambda x: 2 * x[0] + 5 * x[1] + 3 * x[2],
#     lambda x: 2 * x[0] ** 3 + 5 * x[1] + 3 * x[2],
#     lambda x: 2 * x[0] + 5 * x[1] ** 3 + 3 * x[2],
#     lambda x: 2 * x[0] + 5 * x[1] + 3 * x[2] ** 3
# ]
#
# grad_rs = [
#     lambda x: [
#         2,
#         5,
#         3
#     ],
#     lambda x: [
#         1,
#         0,
#         0
#     ],
#     lambda x: [
#         0,
#         1,
#         0
#     ],
#     lambda x: [
#         0,
#         0,
#         1
#     ]
# ]
#
# # dim = 2
# #
# # f = lambda x: -1 * (2 * x[1] * ((x[0] + 1) ** 2 - x[1] ** 2) ** 0.5 - np.pi * x[0] ** 2)
# #
# # grad_f = lambda x: [
# #     (2 * x[1] * (x[0] + 1)) / (((x[0] + 1) ** 2 - x[1] ** 2) ** 0.5) - 2 * np.pi * x[0],
# #     (2 * ((x[0] + 1) ** 2 - 2 * x[1] ** 2)) / (((x[0] + 1) ** 2 - x[1] ** 2) ** 0.5)
# # ]
# #
# # rs = [
# #     lambda x: x[1] - 1,
# #     lambda x: 2 * x[0] - x[1],
# #     lambda x: - x[0],
# #     lambda x: - x[1]
# # ]
# #
# # grad_rs = [
# #     lambda x: [
# #         0,
# #         1
# #     ],
# #     lambda x: [
# #         2,
# #         -1
# #     ],
# #     lambda x: [
# #         -1,
# #         0
# #     ],
# #     lambda x: [
# #         0,
# #         -1
# #     ]
# # ]
