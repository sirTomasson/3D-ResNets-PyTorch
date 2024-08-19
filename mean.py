def get_mean_std(value_scale, dataset):
    assert dataset in ['activitynet', 'kinetics', 'workoutform', '0.5']

    if dataset == 'activitynet':
        mean = [0.4477, 0.4209, 0.3906]
        std = [0.2767, 0.2695, 0.2714]
    elif dataset == 'kinetics':
        mean = [0.4345, 0.4051, 0.3775]
        std = [0.2768, 0.2713, 0.2737]
    elif dataset == 'workoutform':
        mean = [0.41715325, 0.39402192, 0.35711448]
        std = [0.25924891, 0.24782488, 0.23383827]
    elif dataset == '0.5':
        mean = [0.5, 0.5, 0.5]
        std = [0.5, 0.5, 0.5]

    mean = [x * value_scale for x in mean]
    std = [x * value_scale for x in std]

    return mean, std