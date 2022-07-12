import pixelComparer, argparse

class Runner():
    """Run pixel comparison."""

    def __init__(self):
        """Assign parameters and execute training."""
        self.parse_arguments()

    def parse_arguments(self):
        """Process arguments when called from cli."""
        parser = argparse.ArgumentParser(prog='Pixel comparison runner', description='A module that runs pixel by pixel comparison between images, by Qualiti.ai', add_help=True)
        # Defaults for training
        parser.add_argument('-o', '--overtime', type=str, action='store', default='true', help='Specify whether to compare pixels of images over time, or all to the current, last image')
        parser.add_argument('-i', '--imagePaths', nargs='*', type=str, action='store', default='images', help='Specify the list of image paths to be processed')
        args = parser.parse_args()
        # image list
        self.image_paths = args.imagePaths
        # process images over time, vs comparing to the last image
        self.overtime = True
        if args.overtime == 'true':
            self.overtime = True
        elif args.overtime == 'false':
            self.overtime = False

    def run(self):
        """Run comparison based on input."""
        pc = pixelComparer.PixelComparer()
        comparison_percentage_list = pc.run(self.image_paths, self.overtime)
        return comparison_percentage_list

if __name__ == '__main__':
    t = Runner()
    t.run()

# python3 runner.py -o true -i second_image.png first_image.png second_image.png second_image.png second_image.png second_image.png

