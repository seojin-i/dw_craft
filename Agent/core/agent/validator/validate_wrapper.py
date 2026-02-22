"""
각 함수마다 오류가 없는지 검사하기 위한 검증 도구입니다.
"""
import functools
class ValidateWrapper:
    """
    함수의 실행 결과를 검사하는 래퍼 함수입니다.
    """
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __get__(self, instance, owner):
        # 인스턴스에 바인딩
        return lambda *args, **kwargs: self(instance, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        try:
            result = self.func(*args, **kwargs)
            # 결과가 None이 아닌지 검사
            return result
        except Exception as e:
            print(f"Error in function {self.func.__name__}: {e}")
            raise

    # def validate(self):
    #     def wrapper(self, *args, **kwargs):
    #         try:
    #             result = self.func(self, *args, **kwargs)
    #             # 결과가 None이 아닌지 검사
    #             return result
    #         except Exception as e:
    #             print(f"Error in function {self.func.__name__}: {e}")
    #             raise
    #     return wrapper
