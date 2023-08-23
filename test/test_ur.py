from source.ur import RecordingState, UsageRecorder


recorder = UsageRecorder()
recorder.row = 4


def test_check_state_begin_state():
    recorder.sheet1["b4"] = None
    recorder.sheet1["c4"] = None
    recorder.sheet1["d4"] = None
    recorder.sheet1["e4"] = None
    recorder.sheet1["f4"] = None
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = None
    assert recorder.check_state() == RecordingState.WAITING_FOR_INPUT_BEGIN_TIME


def test_check_state_end_state_1():
    recorder.sheet1["b4"] = "User"
    recorder.sheet1["c4"] = "Account"
    recorder.sheet1["d4"] = "Purpose"
    recorder.sheet1["e4"] = "Server"
    recorder.sheet1["f4"] = "2023-10-01 10:00"
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = "Remarks"
    assert recorder.check_state() == RecordingState.WAITING_FOR_INPUT_END_TIME


def test_check_state_end_state_2():
    recorder.sheet1["b4"] = "User"
    recorder.sheet1["c4"] = "Account"
    recorder.sheet1["d4"] = "Purpose"
    recorder.sheet1["e4"] = "Server"
    recorder.sheet1["f4"] = "2023-10-01 10:00"
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = None
    assert recorder.check_state() == RecordingState.WAITING_FOR_INPUT_END_TIME


def test_check_state_abnormal_state_1():
    recorder.sheet1["b4"] = None
    recorder.sheet1["c4"] = "Account"
    recorder.sheet1["d4"] = "Purpose"
    recorder.sheet1["e4"] = "Server"
    recorder.sheet1["f4"] = "2023-10-01 10:00"
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = "Remarks"
    assert recorder.check_state() == RecordingState.ABNORMAL_STATE


def test_check_state_abnormal_state_2():
    recorder.sheet1["b4"] = "User"
    recorder.sheet1["c4"] = None
    recorder.sheet1["d4"] = "Purpose"
    recorder.sheet1["e4"] = "Server"
    recorder.sheet1["f4"] = "2023-10-01 10:00"
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = "Remarks"
    assert recorder.check_state() == RecordingState.ABNORMAL_STATE


def test_check_state_abnormal_state_3():
    recorder.sheet1["b4"] = "User"
    recorder.sheet1["c4"] = "Account"
    recorder.sheet1["d4"] = None
    recorder.sheet1["e4"] = "Server"
    recorder.sheet1["f4"] = "2023-10-01 10:00"
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = "Remarks"
    assert recorder.check_state() == RecordingState.ABNORMAL_STATE


def test_check_state_abnormal_state_4():
    recorder.sheet1["b4"] = "User"
    recorder.sheet1["c4"] = "Account"
    recorder.sheet1["d4"] = "Purpose"
    recorder.sheet1["e4"] = None
    recorder.sheet1["f4"] = "2023-10-01 10:00"
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = "Remarks"
    assert recorder.check_state() == RecordingState.ABNORMAL_STATE


def test_check_state_abnormal_state_5():
    recorder.sheet1["b4"] = None
    recorder.sheet1["c4"] = "Account"
    recorder.sheet1["d4"] = "Purpose"
    recorder.sheet1["e4"] = "Server"
    recorder.sheet1["f4"] = None
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = "Remarks"
    assert recorder.check_state() == RecordingState.ABNORMAL_STATE


def test_check_state_abnormal_state_6():
    recorder.sheet1["b4"] = "User"
    recorder.sheet1["c4"] = None
    recorder.sheet1["d4"] = "Purpose"
    recorder.sheet1["e4"] = "Server"
    recorder.sheet1["f4"] = None
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = "Remarks"
    assert recorder.check_state() == RecordingState.ABNORMAL_STATE


def test_check_state_abnormal_state_7():
    recorder.sheet1["b4"] = "User"
    recorder.sheet1["c4"] = "Account"
    recorder.sheet1["d4"] = None
    recorder.sheet1["e4"] = "Server"
    recorder.sheet1["f4"] = None
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = "Remarks"
    assert recorder.check_state() == RecordingState.ABNORMAL_STATE


def test_check_state_abnormal_state_8():
    recorder.sheet1["b4"] = "User"
    recorder.sheet1["c4"] = "Account"
    recorder.sheet1["d4"] = "Purpose"
    recorder.sheet1["e4"] = None
    recorder.sheet1["f4"] = None
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = "Remarks"
    assert recorder.check_state() == RecordingState.ABNORMAL_STATE


def test_check_state_abnormal_state_9():
    recorder.sheet1["b4"] = "User"
    recorder.sheet1["c4"] = "Account"
    recorder.sheet1["d4"] = "Purpose"
    recorder.sheet1["e4"] = "Server"
    recorder.sheet1["f4"] = None
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = None
    assert recorder.check_state() == RecordingState.ABNORMAL_STATE


def test_check_state_abnormal_state_10():
    recorder.sheet1["b4"] = None
    recorder.sheet1["c4"] = None
    recorder.sheet1["d4"] = None
    recorder.sheet1["e4"] = None
    recorder.sheet1["f4"] = None
    recorder.sheet1["g4"] = None
    recorder.sheet1["h4"] = "Remarks"
    assert recorder.check_state() == RecordingState.ABNORMAL_STATE
