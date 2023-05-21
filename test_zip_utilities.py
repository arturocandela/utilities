# test_mi_modulo.py
import unittest
 
from zip_utils import listar_archivos_zip,crear_ficheros_json_del_zip

class TestListarArchivosZip(unittest.TestCase):

    def test_listar_archivos_zip(self):

        expected = ["test_helper/test_zip_utilities\\file1.zip","test_helper/test_zip_utilities\\file4.ZIP"]
        target = listar_archivos_zip("test_helper/test_zip_utilities")


        self.assertEquals(expected,target)
    
    def test_crear_ficheros_json_del_zip(self):
        self.fail("Not implemented")

if __name__ == "__main__":
    unittest.main()