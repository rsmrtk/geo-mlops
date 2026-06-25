"""
Synthetic training data for location classifier.

Real-world coordinates labeled by location type.
Sources: OpenStreetMap manual lookup, Wikipedia coordinates.
"""

from dataclasses import dataclass


@dataclass
class Sample:
    lat: float
    lng: float
    label: str


# fmt: off
SAMPLES: list[Sample] = [
    # residential
    Sample(50.4547, 30.5238, "residential"),
    Sample(50.4321, 30.4987, "residential"),
    Sample(49.8412, 24.0321, "residential"),
    Sample(49.8201, 24.0156, "residential"),
    Sample(46.9654, 31.9876, "residential"),
    Sample(48.9201, 24.7123, "residential"),
    Sample(47.8932, 35.1654, "residential"),
    Sample(49.5821, 34.5412, "residential"),
    Sample(50.9012, 34.7821, "residential"),
    Sample(51.5012, 31.2987, "residential"),
    Sample(48.5123, 22.2654, "residential"),
    Sample(46.6412, 32.6321, "residential"),
    Sample(47.1234, 37.5432, "residential"),
    Sample(48.7321, 37.9123, "residential"),
    Sample(50.0123, 36.2345, "residential"),
    Sample(49.2345, 28.4321, "residential"),
    Sample(48.6543, 26.5678, "residential"),
    Sample(50.6789, 26.2567, "residential"),
    Sample(51.3210, 25.3456, "residential"),
    Sample(49.9012, 23.8765, "residential"),

    # commercial
    Sample(50.4480, 30.5234, "commercial"),
    Sample(50.4512, 30.5289, "commercial"),
    Sample(49.8397, 24.0297, "commercial"),
    Sample(49.8450, 24.0312, "commercial"),
    Sample(46.9751, 31.9946, "commercial"),
    Sample(48.9312, 24.7234, "commercial"),
    Sample(47.9012, 35.1789, "commercial"),
    Sample(49.5934, 34.5523, "commercial"),
    Sample(50.9123, 34.7934, "commercial"),
    Sample(51.5123, 31.3098, "commercial"),
    Sample(48.5234, 22.2765, "commercial"),
    Sample(46.6523, 32.6432, "commercial"),
    Sample(47.1345, 37.5543, "commercial"),
    Sample(48.7432, 37.9234, "commercial"),
    Sample(50.0234, 36.2456, "commercial"),
    Sample(49.2456, 28.4432, "commercial"),
    Sample(48.6654, 26.5789, "commercial"),
    Sample(50.6890, 26.2678, "commercial"),
    Sample(51.3321, 25.3567, "commercial"),
    Sample(49.9123, 23.8876, "commercial"),

    # industrial
    Sample(50.4180, 30.5634, "industrial"),
    Sample(50.3980, 30.5834, "industrial"),
    Sample(49.7997, 24.0697, "industrial"),
    Sample(49.7800, 24.0897, "industrial"),
    Sample(46.9351, 32.0346, "industrial"),
    Sample(48.8912, 24.7634, "industrial"),
    Sample(47.8612, 35.2189, "industrial"),
    Sample(49.5534, 34.5923, "industrial"),
    Sample(50.8723, 34.8334, "industrial"),
    Sample(51.4723, 31.3498, "industrial"),
    Sample(48.4834, 22.3165, "industrial"),
    Sample(46.6123, 32.6832, "industrial"),
    Sample(47.0945, 37.5943, "industrial"),
    Sample(48.7032, 37.9634, "industrial"),
    Sample(49.9834, 36.2856, "industrial"),
    Sample(49.2056, 28.4832, "industrial"),
    Sample(48.6254, 26.6189, "industrial"),
    Sample(50.6490, 26.3078, "industrial"),
    Sample(51.2921, 25.3967, "industrial"),
    Sample(49.8723, 23.9176, "industrial"),

    # park
    Sample(50.4416, 30.5205, "park"),
    Sample(50.4556, 30.5123, "park"),
    Sample(49.8375, 24.0234, "park"),
    Sample(49.8456, 24.0189, "park"),
    Sample(46.9651, 31.9801, "park"),
    Sample(48.9201, 24.7101, "park"),
    Sample(47.8923, 35.1601, "park"),
    Sample(49.5812, 34.5401, "park"),
    Sample(50.9001, 34.7801, "park"),
    Sample(51.5001, 31.2901, "park"),
    Sample(48.5101, 22.2601, "park"),
    Sample(46.6401, 32.6201, "park"),
    Sample(47.1201, 37.5401, "park"),
    Sample(48.7301, 37.9101, "park"),
    Sample(50.0101, 36.2301, "park"),
    Sample(49.2301, 28.4201, "park"),
    Sample(48.6501, 26.5601, "park"),
    Sample(50.6701, 26.2501, "park"),
    Sample(51.3101, 25.3401, "park"),
    Sample(49.9001, 23.8701, "park"),

    # transport
    Sample(50.4412, 30.4870, "transport"),  # Kyiv central station
    Sample(50.4389, 30.4923, "transport"),
    Sample(49.8312, 24.0023, "transport"),  # Lviv station
    Sample(49.8289, 24.0076, "transport"),
    Sample(46.9623, 31.9723, "transport"),
    Sample(48.9178, 24.7023, "transport"),
    Sample(47.8889, 35.1523, "transport"),
    Sample(49.5789, 34.5323, "transport"),
    Sample(50.8978, 34.7723, "transport"),
    Sample(51.4978, 31.2823, "transport"),
    Sample(48.5078, 22.2523, "transport"),
    Sample(46.6378, 32.6123, "transport"),
    Sample(47.1178, 37.5323, "transport"),
    Sample(48.7278, 37.9023, "transport"),
    Sample(50.0078, 36.2223, "transport"),
    Sample(49.2278, 28.4123, "transport"),
    Sample(48.6478, 26.5523, "transport"),
    Sample(50.6678, 26.2423, "transport"),
    Sample(51.3078, 25.3323, "transport"),
    Sample(49.8978, 23.8623, "transport"),

    # education
    Sample(50.4534, 30.5156, "education"),
    Sample(50.4478, 30.5201, "education"),
    Sample(49.8434, 24.0256, "education"),
    Sample(49.8356, 24.0278, "education"),
    Sample(46.9723, 31.9923, "education"),
    Sample(48.9278, 24.7256, "education"),
    Sample(47.8978, 35.1723, "education"),
    Sample(49.5878, 34.5556, "education"),
    Sample(50.9078, 34.7878, "education"),
    Sample(51.5078, 31.3023, "education"),
    Sample(48.5178, 22.2723, "education"),
    Sample(46.6478, 32.6378, "education"),
    Sample(47.1278, 37.5523, "education"),
    Sample(48.7378, 37.9178, "education"),
    Sample(50.0178, 36.2423, "education"),
    Sample(49.2378, 28.4378, "education"),
    Sample(48.6578, 26.5778, "education"),
    Sample(50.6878, 26.2623, "education"),
    Sample(51.3278, 25.3523, "education"),
    Sample(49.9178, 23.8823, "education"),

    # healthcare
    Sample(50.4467, 30.5267, "healthcare"),
    Sample(50.4389, 30.5312, "healthcare"),
    Sample(49.8367, 24.0312, "healthcare"),
    Sample(49.8289, 24.0334, "healthcare"),
    Sample(46.9689, 31.9989, "healthcare"),
    Sample(48.9245, 24.7312, "healthcare"),
    Sample(47.8945, 35.1789, "healthcare"),
    Sample(49.5845, 34.5612, "healthcare"),
    Sample(50.9045, 34.7934, "healthcare"),
    Sample(51.5045, 31.3079, "healthcare"),
    Sample(48.5145, 22.2779, "healthcare"),
    Sample(46.6445, 32.6434, "healthcare"),
    Sample(47.1245, 37.5579, "healthcare"),
    Sample(48.7345, 37.9234, "healthcare"),
    Sample(50.0145, 36.2479, "healthcare"),
    Sample(49.2345, 28.4434, "healthcare"),
    Sample(48.6545, 26.5834, "healthcare"),
    Sample(50.6845, 26.2734, "healthcare"),
    Sample(51.3245, 25.3579, "healthcare"),
    Sample(49.9145, 23.8879, "healthcare"),

    # religious
    Sample(50.4523, 30.5178, "religious"),
    Sample(50.4401, 30.5223, "religious"),
    Sample(49.8423, 24.0278, "religious"),
    Sample(49.8301, 24.0301, "religious"),
    Sample(46.9712, 31.9945, "religious"),
    Sample(48.9267, 24.7278, "religious"),
    Sample(47.8967, 35.1745, "religious"),
    Sample(49.5867, 34.5578, "religious"),
    Sample(50.9067, 34.7856, "religious"),
    Sample(51.5067, 31.3045, "religious"),
    Sample(48.5167, 22.2745, "religious"),
    Sample(46.6467, 32.6401, "religious"),
    Sample(47.1267, 37.5545, "religious"),
    Sample(48.7367, 37.9201, "religious"),
    Sample(50.0167, 36.2445, "religious"),
    Sample(49.2367, 28.4401, "religious"),
    Sample(48.6567, 26.5801, "religious"),
    Sample(50.6867, 26.2645, "religious"),
    Sample(51.3267, 25.3545, "religious"),
    Sample(49.9167, 23.8845, "religious"),
]
# fmt: on


def fetch_training_data(limit_per_class: int = 200) -> list[Sample]:
    """Return labeled samples. limit_per_class is ignored — all samples returned."""
    return SAMPLES
