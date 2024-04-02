from enum import Enum
import subprocess
import random
import os

class Language(Enum):
    PYTHON = 1


class ExecutionStatus(Enum):
    NYR = 0  # 실행중. 결과를 얻는 데 몇 시간이 더 걸릴 수 있음
    ACC = 1  # 성공적으로 실행. 솔루션이 올바름
    WRA = 2  # 성공적으로 실행. 솔루션이 잘못됨
    TLE = 3  # 실행되었지만 시간 제한 초과
    COE = 4  # 컴파일 실패
    RTE = 5  # 실행 중 오류 발생
    INE = 6  # 내부 오류 발생. 다시 시도하라는 메시지 표시


class TestCase:
    input_data = None
    output_data = None

    def __init__(self, input_data, expected_output):
        self.input_data = input_data
        self.output_data = expected_output

    def get_input(self):
        return self.input_data

    def get_output(self):
        return self.output_data


def generate_test_case(input_data, expected_output):    
    inputs = ""
    for x in input_data:
        inputs += x + "\n"

    outputs = ""
    for x in expected_output:
        outputs += x + "\n"

    # print(inputs + outputs)
    test_case = TestCase(inputs, outputs)
    return test_case


def generate_rand_name(length):
    generated = ""
    for i in range(length):
        base = 97 if random.randint(0, 1) == 0 else 65
        offset = random.randint(0, 25)
        generated += chr(base+offset)
    return generated

class Compiler:
    exec_status = None
    code = None
    test_case = None
    outputs = None
    errors = None
    language = None
    filename = None
    hasErrors = False
    hasExecuted = False
    hasFile = False
    maxExecTime = 5

    def add_test_case(self, test_case):
        # print("** Test case added **")
        if isinstance(test_case, TestCase):
            self.test_case = test_case
        else:
            raise ValueError("Trying to add Invalid test case!")
        return

    def set_language(self, l):
        if isinstance(l, Language):
            self.language = l
        else:
            self.language = None
            raise ValueError("Invalid language")

    def set_code(self, code):
        self.code = code
        return

    def set_max_exec_time(self, time_in_seconds):
        self.maxExecTime = time_in_seconds
        return

    # 각 테스트케이스에 따른 결과 목록 반환
    def get_output(self):
        if self.hasExecuted:
            return self.outputs
        else:
            return None

    # 각 테스트케이스에 따른 오류 목록 반환
    def get_errors(self):
        if self.hasErrors:
            return self.errors
        else:
            return None

    def contains_errors(self):
        return self.hasErrors

    def generate_code_file(self):
        self.filename = generate_rand_name(10)
        if self.filename is None:
            print("*** ERROR : Filename cannot be generated! ***")
        complete_code = self.code + "\r\n"
        
        
        file_handle = open(self.filename, "w")
        file_handle.write(complete_code)
        file_handle.flush()
        file_handle.close()

    def delete_code_file(self):
        if self.filename is None:
            print("*** ERROR: filename NONE ***")
        os.remove(self.filename)
        self.hasFile = False
        self.filename = None

    def compare_outputs(self):
        values = []
        expected_output = self.test_case.get_output()
        actual_output = self.outputs[0]

        # Debug
        # print("## len(self.outputs) = " + str(len(self.outputs)))
        # print("# EX: " + expected_output)
        # print("# len : " + str(len(str(expected_output))))
        # print("# AC: " + actual_output)
        # print("# len : " + str(len(str(actual_output))))
        # print("# Comparison : " + str(expected_output == actual_output))
        # print("\n")
        # Debug

        values.append(expected_output == actual_output)

        # Debug
        # print("Values .... ")
        # for v in values:
        #     print(str(v))
        # Debug

        return values

    def execute(self):
        self.exec_status = ExecutionStatus.NYR

        if self.language is not None:

            if not self.hasFile or self.filename is None:
                self.generate_code_file()

            if self.language == Language.PYTHON:
                command = ["python", self.filename]

                if self.outputs is None:
                    self.outputs = []

                if self.errors is None:
                    self.errors = []

                process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

                try:
                    o, e = process.communicate(str(self.test_case.get_input()).encode('utf-8'), timeout=self.maxExecTime)
                    self.outputs.append(o.decode('utf-8'))

                    if len(e) != 0:
                        self.errors.append(e.decode('utf-8'))
                        self.hasErrors = True
                    else:
                        self.errors.append(None)

                    self.hasExecuted = True

                except subprocess.TimeoutExpired:
                    print("*** TIMEOUT, killing process... ***")
                    if process is not None:
                        process.kill()
                    self.hasExecuted = False
                    self.exec_status = ExecutionStatus.TLE

                if self.hasExecuted:
                    comparisons = self.compare_outputs()
                    if False in comparisons:
                        self.exec_status = ExecutionStatus.WRA
                    else:
                        self.exec_status = ExecutionStatus.ACC
            else:
                print("*** Error : Unknown Programming language Selected ****")
                self.exec_status = ExecutionStatus.INE
        else:
            print("*** Error : No Programming Language Selected ***")
            self.exec_status = ExecutionStatus.INE
        return self.exec_status
