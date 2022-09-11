import unittest
import reproducibility.reproducibility as reproducibility


class ReproducibilityTests(unittest.TestCase):
    # set up the cell for testing
    def setUp(self) -> None:
        # retrieve the directory to write to
        self.file_dir = reproducibility.get_file_dir()
        # define expected output
        self.output = ""

    # test save functions
    def test_save_exp_spec_list(self) -> None:
        # confirm we can save the explicit specification list
        output = reproducibility.save_exp_spec_list(file_dir=self.file_dir)
        self.assertEqual(output.decode(), self.output)

    def test_save_env_yml(self) -> None:
        # confirm we can save the environment YAML file
        output = reproducibility.save_env_yml(file_dir=self.file_dir)
        self.assertEqual(output.decode(), self.output)

    def test_save_xenv_yml(self) -> None:
        # confirm we can save the cross platform environment YAML file
        output = reproducibility.save_xenv_yml(file_dir=self.file_dir)
        self.assertEqual(output.decode(), self.output)
