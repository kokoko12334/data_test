import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 출력할 변수
variable = "Hello, world!"

# 변수 값을 로그로 출력
logging.debug(f"The value of the variable is: {variable}")
logging.info(f"This is an information message.")
logging.warning(f"This is a warning message.")