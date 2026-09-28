"""Testes offline da verificação local de assets, sem download obrigatório."""
import struct
import tempfile
import unittest
import zlib
import random
from pathlib import Path
from verificar_imagens import IMAGES, PNG_HEADER, faltantes, imagem_valida


def sample_png():
    rng = random.Random(33)
    rgba = bytes(rng.randrange(256) for _ in range(48 * 48 * 4))
    scan = b''.join(b'\0' + rgba[row*48*4:(row+1)*48*4] for row in range(48))
    def chunk(name, content):
        return struct.pack('>I', len(content)) + name + content + struct.pack('>I', zlib.crc32(name + content))
    return PNG_HEADER + chunk(b'IHDR', struct.pack('>IIBBBBB', 48, 48, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(scan)) + chunk(b'IEND', b'')


class AssetTests(unittest.TestCase):
    def test_missing_assets_reported_without_network(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(faltantes(Path(folder)), list(IMAGES))

    def test_original_names_and_png_integrity(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            name = IMAGES[0]
            (root / name).write_bytes(sample_png())
            self.assertTrue(imagem_valida(name, root))
            self.assertEqual(len(faltantes(root)), len(IMAGES) - 1)
            (root / name).write_bytes(b'not a png')
            self.assertFalse(imagem_valida(name, root))


if __name__ == '__main__':
    unittest.main()
