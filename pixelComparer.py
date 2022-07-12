import os, time, subprocess

class PixelComparer():
    def __init__(self):
        pass

    def run_pixel_comparison(self, image_path1, image_path2, diff):
        compare_cmd = 'compare -metric RMSE -subimage-search -dissimilarity-threshold 1.0 "%s" "%s" "%s"' \
                      % (image_path1, image_path2, diff)

        attempts = 0
        while attempts < 2:
            proc = subprocess.Popen(compare_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            out, err = proc.communicate()
            # print('Comparison output: %s' % err)
            diff = err.split()[1][1:-1]

            try:
                trimmed = float("{:.2f}".format(float(diff)))
                return trimmed
            except ValueError:
                if attempts == 0:
                    print('Comparison failed first time. Output %s' % err)
                    compare_cmd = 'magick ' + compare_cmd
                else:
                    raise Exception('Could not parse comparison output: %s' % err)
            finally:
                attempts += 1

    # calculate pixel comparisons between all input images and the final image
    def run_pixel_comparison_last_run(self, image_paths):
        second_path = image_paths[-1]
        diff_list = []
        for i in range(len(image_paths) - 1):
            diff_path = 'diff_output_' + str(i) + '.png'
            first_path = image_paths[i]
            diff = self.run_pixel_comparison(first_path, second_path, diff_path)
            diff_list.append(diff)
            print(first_path, second_path, diff)
        return diff_list

    # calculate pixel comparisons between all input images sequentially
    def run_pixel_comparison_over_time(self, image_paths):
        diff_list = []
        for i in range(len(image_paths) - 1):
            diff_path = 'diff_output_' + str(i) + '.png'
            first_path = image_paths[i]
            second_path = image_paths[i+1]
            diff = self.run_pixel_comparison(first_path, second_path, diff_path)
            diff_list.append(diff)
            print(first_path, second_path, diff)
        return diff_list

    def run_bash_command(self, bash_command):
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        while process.poll() is None:
            time.sleep(0.1)

    def run(self, image_paths, is_over_time):

        # Verify that image paths exist
        for image_path in image_paths:
            if not os.path.exists(image_path):
                print('Incorrect image path')
                return []

        # Run pixel comparison between images
        if is_over_time:
            # returns list of floats (percentage similarity)
            diff_list = self.run_pixel_comparison_over_time(image_paths)
        else:
            # returns list of floats (percentage similarity)
            diff_list = self.run_pixel_comparison_last_run(image_paths)
        
        return diff_list

