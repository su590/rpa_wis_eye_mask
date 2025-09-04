wis_eye_mask_rpa：
    对redis的逻辑做了一个修改
    在Session的__enter__()代码当中新加了一个check()的操作
    在这个操作当中直接去验证当前cookie的可行性（异常已经进行了相应的封装）