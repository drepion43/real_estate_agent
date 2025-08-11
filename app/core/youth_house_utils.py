import yaml
import pandas as pd

# Type dict and environment
from typing import Any, Dict, List, TypedDict

def data_load_from_excel(file_path, sheet_name=None):
    """
    액셀 파일에서 특정 시트 혹은 모든 시트 로드 후 데이터 변환
    - file path: 액셀 파일 경로
    - sheet_name : 엑셀 파일 내 특정 시트명
    """
    
    if sheet_name:
        data = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
        return {sheet_name: data}
    else:
        return pd.read_excel(file_path, sheet_name=None, engine='openpyxl')

# yaml 파일 불러오기 --> 보안 및 에러 핸들링 코드 추가
def load_yaml_description(file_path: str) -> Dict[str, Any]:
    info_yaml = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            info_yaml = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"파일 경로 오류: 주어진 파일 경로는 존재하지 않은 경로입니다.")
    except yaml.YAMLError as err:
        print(f"YAML 파일 파싱 오류: YAML 파일의 형식, 문법 오류{err}가 발생하였습니다.")
    except Exception as err:
        print(f"예외 처리 오류: 예기치 못한 오류 {err}가 발생하였습니다.")
        
    return info_yaml