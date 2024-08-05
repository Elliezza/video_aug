import argparse, os
import cv2


def gen_capture(filename, output):
    cap = cv2.VideoCapture(filename)
    # 读取第一帧
    ret, frame = cap.read()
    if ret:
        filename = os.path.splitext(os.path.basename(filename))[0]
        outfile = os.path.join(output, filename+'.jpg')
        # 保存第一帧为图片
        cv2.imwrite(outfile, frame)
        
    # 释放视频捕捉对象
    cap.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process videos.')
    parser.add_argument('-f', '--file', type=str, help='file path')
    parser.add_argument('-o', '--output', default='./', type=str, help='output file path')


    args = parser.parse_args()

    filename = args.file
    output = args.output

    gen_capture(filename, output)
