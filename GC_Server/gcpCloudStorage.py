from datetime import datetime
from google.cloud import storage
import random
import string

def upload(file, bucket_name, filepath='', unique_filename=False):
	if not(file or bucket_name):
		print('[#] Args Required (File, Bucket_name)')
		return False

	cs = storage.Client('backup-c8eab')
	bucket = cs.get_bucket(bucket_name) # 인자의 bucket_name으로 GCP 연결 시도 

	''' 파일이 Byte 형태가 아닐 시 적용
	filename = file.name
	if unique_filename: # 날짜 데이터를 조합한 이름 생성
		filename = datetime.now().strftime("%Y%m%d_%H%M%S") + file.name
	'''
	filename = datetime.now().strftime("%Y%m%d_%H%M%S")

	blob = bucket.blob(filepath + '/' + filename + '.png') # filepath에 맞추어 파일 생성. 수정할 경우 폴더 생성 후 그 안의 파일 생성.
	blob.upload_from_file(file)
	blob.make_public() # public 설정을 통한 일반 사용자 접근 허용

	url = blob.public_url

	return url