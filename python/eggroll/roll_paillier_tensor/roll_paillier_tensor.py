#  Copyright (c) 2019 - now, Eggroll Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import roll_paillier_tensor as rpt_engine

<<<<<<< HEAD
=======
from eggroll.roll_pair.roll_pair import RollPairContext
from eggroll.utils import log_utils

LOGGER = log_utils.get_logger()
>>>>>>> remotes/origin/v2.x
class RptBaseEngine:
    def load(self, x):
        raise NotImplementedError("todo")
    def add(self, x, y):
        raise NotImplementedError("todo")

class RptGpuEngine(RptBaseEngine):
    def __init__(self, pub_key=None, priv_key=None):
        self.pub_key = pub_key
        self.priv_key = priv_key

    def __setstate__(self, state):
        bin_pub, bin_prv = state
        self.pub_key = rpt_engine.gpu_load_pub_key(bin_pub)
        self.priv_key = rpt_engine.gpu_load_priv_key(bin_prv)

    def __getstate__(self):
        return rpt_engine.gpu_dump_pub_key(self.pub_key), rpt_engine.gpu_dump_prv_key(self.priv_key)

    def add(self, x, y):
        return rpt_engine.gpu_dotadd(x, y, self.pub_key)

    def vdot(self, x, y):
        return rpt_engine.gpu_dotmul(x, y, self.pub_key)

    def matmul(self, x, y):
        return rpt_engine.gpu_matmul(x, y, self.pub_key)

    def encrypt(self, x, y):
        return rpt_engine.gpu_encrypt(x, y, self.pub_key)

    def decrypt(self, x, y):
        return rpt_engine.gpu_decrypt(x, y, self.pub_key)

    def load(self, x):
        return rpt_engine.gpu_load(x)

    def dump(self, x):
        return rpt_engine.gpu_dump(x)


class RptCpuEngine(RptBaseEngine):
    def __init__(self, pub_key=None, priv_key=None):
        self.pub_key = pub_key
        self.priv_key = priv_key

    def __setstate__(self, state):
        bin_pub, bin_prv = state
        self.pub_key = rpt_engine.load_pub_key(bin_pub)
        self.priv_key = rpt_engine.load_prv_key(bin_prv)

    def __getstate__(self):
        return rpt_engine.dump_pub_key(self.pub_key), rpt_engine.dump_prv_key(self.priv_key)

    def add(self, x, y):
        return rpt_engine.add(x, y, self.pub_key, self.priv_key)

    def vdot(self, x, y):
        return rpt_engine.vdot(x, y, self.pub_key, self.priv_key)

    def scalar_mul(self, x, scale):
        return rpt_engine.scalar_mul(x, scale, self.pub_key, self.priv_key)

    def matmul(self, x, y):
        return rpt_engine.matmul(x, y, self.pub_key, self.priv_key)

    def matmul_c_eql(self, x, y):
        return rpt_engine.matmul_c_eql(x, y, self.pub_key, self.priv_key)

    def matmul_r_eql(self, x, y):
        return rpt_engine.matmul_r_eql(x, y, self.pub_key, self.priv_key)

    # tool
    def load(self, x):
        return rpt_engine.load(x)

    def dump(self, x):
        return rpt_engine.dump(x)

    def obf(self, x):
        return rpt_engine.obf(x, self.pub_key, self.priv_key)

    def mean(self, x):
        return rpt_engine.mean(x, self.pub_key, self.priv_key)

    def transe(self, x):
        return rpt_engine.transe(x)

    def hstack(self, x, y):
        return rpt_engine.hstack(x, y, self.pub_key, self.priv_key)

    def encrypt(self, x):
        return rpt_engine.encrypt_and_obfuscate(x, self.pub_key)

    def decrypt(self, x):
        return rpt_engine.decryptdecode(x, self.pub_key, self.priv_key)

    def decode(self, x):
        return rpt_engine.decode(x, self.pub_key, self.priv_key)

    def out(self, x):
        return rpt_engine.print(x, self.pub_key, self.priv_key)

    #interface
    def manager(self, x, y, val):
        return rpt_engine.make_manager(x, y, val, self.pub_key)

    def num2Mng(self, x):
        return rpt_engine.num2Mng(x, self.pub_key)

    def num2Mng_test(self, x):
        return rpt_engine.num2Mng_test(x, self.pub_key)


class RptContext:
    def __init__(self, rp_ctx:RollPairContext):
        self.rp_ctx = rp_ctx

    def load(self, namespace, name, engine_type="cpu"):
        return RollPaillierTensor(self.rp_ctx.load(namespace, name), engine_type)

class Tensor(object):
    def __init__(self):
        pass

class NumpyTensor(Tensor):
    def __init__(self, ndarray, engine_type='cpu'):
        if isinstance(ndarray, int) or isinstance(ndarray, float):
            self._ndarray = np.array([[ndarray]])
        else:
            self._ndarray = ndarray

        if engine_type == 'cpu':
            self.pub_key, self.prv_key = rpt_engine.keygen()
            self._engine = RptCpuEngine(self.pub_key, self.prv_key)
        else:
            print("todo")

    def __add__(self, other):
        if isinstance(other, NumpyTensor):
            return self._ndarray + other._ndarray
        if isinstance(other, RollPaillierTensor):
            return other.add_local(self._ndarray)

    def __sub__(self, other):
        if isinstance(other, NumpyTensor):
            return self._ndarray - other._ndarray
        if isinstance(other, RollPaillierTensor):
            return other.scalar_mul(-1).add_local(self._ndarray)

    def encrypt(self):
        rpt = RollPaillierTensor(self._ndarray)
        return rpt.encrypt()

    def out(self, str = "[CHAN ZHEN NAN]"):
        print(str)
        print(self._ndarray)

    def T(self):
       return NumpyTensor(self._ndarray.T)

    def __rmul__(self, other):
        print("__rmul__")
        return

    def __mul__(self, other):
        if isinstance(other, NumpyTensor):
            return self._ndarray * other._ndarray
        if isinstance(other, RollPaillierTensor):
            return other.mul(self._ndarray)


    def __matmul__(self, other):
        if isinstance(other, NumpyTensor):
            return NumpyTensor(self._ndarray.dot(other._ndarray))
        if isinstance(other, RollPaillierTensor):
            return other.matmul_local(self._ndarray)

    def __rmatmul__(self, other):
        print("__rmatmul__")
        return

    def __setstate__(self):
        pass

    def __getstate__(self):
        pass

class PaillierTensor(Tensor):
    def __init__(self, store, engine_type='cpu'):
        self._store = store
        if engine_type == 'cpu':
            self.pub_key, self.prv_key = rpt_engine.keygen()
            self._engine = RptCpuEngine(self.pub_key, self.prv_key)
        else:
            print("todo")


    def __add__(self, other):
        if isinstance(other, NumpyTensor):
            return self.add(other._ndarray)
        if isinstance(other, PaillierTensor):
            return self.add(other._store)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.scalar_mul(other)
        if isinstance(other, PaillierTensor):
            return self.mul(other)
        if isinstance(other, NumpyTensor):
            return self.mul(other)


    #function
    def add(self, other):
        if isinstance(vec1, np.ndarray) and isinstance(vec2, np.ndarray):
            return vec1 + vec2
        if isinstance(vec1, np.ndarray):
            m1 = self._engine.num2Mng(vec1)
        else:
            m1 = self._engine.load(vec1)
        if isinstance(vec2, np.ndarray):
            m2 = self._engine.num2Mng(vec2)
        else:
            m2 = self._engine.load(vec2)
        return PaillierTensor(self._engine.add(m1, m2))

    def mul(self, other):
        if isinstance(self._store, np.ndarray) and isinstance(other, np.ndarray):
            return self._store * other
        if isinstance(self._store, np.ndarray):
            m1 = self._engine.num2Mng(self._store)
        else:
            m1 = self._engine.load(self._store)
        if isinstance(other, np.ndarray):
            m2 = self._engine.num2Mng(other)
        else:
            m2 = self._engine.load(other)
        return PaillierTensor(self._engine.vdot(m1, m2))


class RollPaillierTensor(Tensor):
    def __init__(self, store, engine_type='cpu'):
        self._store = store
        if engine_type == 'cpu':
            self.pub_key, self.prv_key = rpt_engine.keygen()
            self._engine = RptCpuEngine(self.pub_key, self.prv_key)
        else:
            print("todo")

    def __add__(self, other):
        if isinstance(other, NumpyTensor):
            return self.add_local(other._ndarray)
        if isinstance(other, RollPaillierTensor):
            return self.add(other)

    def __sub__(self, other):
        if isinstance(other, NumpyTensor):
            return self.add_local(other._ndarray * (-1))

        if isinstance(other, RollPaillierTensor):
            return self.add(other.scalar_mul(-1))

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.scalar_mul(other)
        if isinstance(other, RollPaillierTensor):
            return self.mul(other)
        if isinstance(other, NumpyTensor):
            return self.mul_local(other._ndarray)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.scalar_mul(float(1 / other))
        if isinstance(other, RollPaillierTensor):
            return


    def __matmul__(self, other):
        if isinstance(other, NumpyTensor):
            print("LLLLLLLLLLLLLLLLLLLLLLLL")
            return self.matmul_local(other._ndarray)

        if isinstance(other, RollPaillierTensor):
            return self.matmul(other)

    #map_value
    def add_local(self, other):
        _engine = self._engine
        def functor(vec1, vec2):
            if isinstance(vec1, np.ndarray) and isinstance(vec2, np.ndarray):
                return vec1 + vec2
            if isinstance(vec1, np.ndarray):
                m1 = _engine.num2Mng(vec1)
            else:
                m1 = _engine.load(vec1)
            if isinstance(vec2, np.ndarray):
                m2 = _engine.num2Mng(vec2)
            else:
                m2 = _engine.load(vec2)
            return _engine.dump(_engine.add(m1, m2))
        return RollPaillierTensor(self._store.map_values(lambda v: functor(v, other)))

    def mul_local(self, other):
        _engine = self._engine
        def functor(vec1, vec2):
            if isinstance(vec1, np.ndarray) and isinstance(vec2, np.ndarray):
                return vec1 * vec2
            if isinstance(vec1, np.ndarray):
                m1 = _engine.num2Mng(vec1)
            else:
                m1 = _engine.load(vec1)
            if isinstance(vec2, np.ndarray):
                m2 = _engine.num2Mng(vec2)
            else:
                m2 = _engine.load(vec2)
            return _engine.dump(_engine.vdot(m1, m2))
        return RollPaillierTensor(self._store.map_values(lambda v: functor(v, other)))

    def matmul_local(self, vec):
        _engine = self._engine
        def seq_op(mat, vec):
            if isinstance(mat, np.ndarray) and isinstance(vec, np.ndarray):
                return mat.dot(vec)
            else:
                mat_enc = _engine.load(mat)
                vec_mng = _engine.num2Mng(vec)
                return _engine.dump(_engine.matmul(mat_enc, vec_mng))
        return RollPaillierTensor(self._store.map_values(lambda v: seq_op(v, vec)))

    def scalar_mul(self, scalar):
        _engine = self._engine
        def seq_op(mat, scalar):
            if  isinstance(mat, np.ndarray):
                return mat * scalar
            else:
                m1 = _engine.load(mat)
                return _engine.dump(_engine.scalar_mul(m1, scalar))
        return RollPaillierTensor(self._store.map_values(lambda v: seq_op(v, scalar)))

    def mean(self):
        _engine = self._engine
        def functor(mat):
            if isinstance(mat, np.ndarray):
                return np.array([[mat.mean()]])
            else:
                pln = _engine.load(mat)
                mean = _engine.mean(pln)
                return _engine.dump(mean)

        return RollPaillierTensor(self._store.map_values(lambda mat: functor(mat)))

    def T(self):
        _engine = self._engine
        def functor(mat):
            if isinstance(mat, np.ndarray):
                return mat.T
            else:
                pln = _engine.load(mat)
                trans = _engine.transe(pln)
                return _engine.dump(trans)
        return RollPaillierTensor(self._store.map_values(lambda mat: functor(mat)))

    def get(self):
        _engine = self._engine
        return list(self._store.get_all())

    def split(self, num, ax):
        _engine = self._engine
        def seq_op(mat, num, ax, id):
            if isinstance(mat, np.ndarray):
                if id == 0:
                    a, b = np.split(mat, (num, ), axis=ax)
                    return a
                else:
                    a, b = np.split(mat, (num, ), axis=ax)
                    return b
            else:
                print("coming soon")
                return b'100'
        a = RollPaillierTensor(self._store.map_values(lambda mat: seq_op(mat, num, ax, 0)))
        b = RollPaillierTensor(self._store.map_values(lambda mat: seq_op(mat, num, ax, 1)))
        return a, b

    #join
    def add(self, other):
        _engine = self._engine
        def functor(vec1, vec2):
            if isinstance(vec1, np.ndarray) and isinstance(vec2, np.ndarray):
                return vec1 + vec2
            if isinstance(vec1, np.ndarray):
                m1 = _engine.num2Mng(vec1)
            else:
                m1 = _engine.load(vec1)
            if isinstance(vec2, np.ndarray):
                m2 = _engine.num2Mng(vec2)
            else:
                m2 = _engine.load(vec2)
            return _engine.dump(_engine.add(m1, m2))
        return RollPaillierTensor(self._store.join(other._store, lambda mat1, mat2: functor(mat1, mat2)))

    def mul(self, other):
        _engine = self._engine
        def functor(vec1, vec2):
            if isinstance(vec1, np.ndarray) and isinstance(vec2, np.ndarray):
                return vec1 * vec2
            if isinstance(vec1, np.ndarray):
                m1 = _engine.num2Mng(vec1)
            else:
                m1 = _engine.load(vec1)
            if isinstance(vec2, np.ndarray):
                m2 = _engine.num2Mng(vec2)
            else:
                m2 = _engine.load(vec2)
            return _engine.dump(_engine.vdot(m1, m2))
        return RollPaillierTensor(self._store.join(other._store, lambda mat1, mat2: functor(mat1, mat2)))

    def matmul(self, other):
        _engine = self._engine
        def seq_op(mat1, mat2):
            if isinstance(mat1, np.ndarray) and isinstance(mat2, np.ndarray):
                print("HHHHHHHHHHHHHHHHHHHHHHHHH")
                print("1111", mat1)
                print("2222", mat2)
                return mat1.dot(mat2)
            if isinstance(mat1, np.ndarray):
                print("CCCCCCCCCC1111111111")
                m1 = _engine.num2Mng_test(mat1)
            else:
                print("CCCCCCCCCC1222222222222")
                m1 = _engine.load(mat1)
            if isinstance(mat2, np.ndarray):
                print("DDDDDDDDDDDD11111111111")
                m2 = _engine.num2Mng_test(mat2)
            else:
                print("DDDDDDDDDDDD2222222222")
                m2 = _engine.load(mat2)
            return _engine.dump(_engine.matmul(m1, m2))
        return RollPaillierTensor(self._store.join(other._store, lambda mat1, mat2 : seq_op(mat1, mat2)))

    def encrypt(self):
        _engine = self._engine
        def functor(mat):
            if isinstance(mat, np.ndarray):
                pln = _engine.num2Mng(mat)
                return _engine.dump(_engine.encrypt(pln))
            else:
                pln = _engine.load(mat)
                return _engine.dump(_engine.encrypt(pln))
        return RollPaillierTensor(self._store.map_values(lambda mat: functor(mat)))

    def hstack(self, other):
        _engine = self._engine
        def seq_op(mat1, mat2):
            if isinstance(mat1, np.ndarray) and isinstance(mat2, np.ndarray):
                return mat1.hstack(mat2)
            if isinstance(mat1, np.ndarray):
                m1 = _engine.num2Mng(mat1)
            else:
                m1 = _engine.load(mat1)

            if isinstance(mat2, np.ndarray):
                m2 = _engine.num2Mng(mat2)
            else:
                m2 = _engine.load(mat2)
            return _engine.dump(_engine.hstack(m1, m2))

        return RollPaillierTensor(self._store.join(other._store, lambda mat1, mat2 : seq_op(mat1, mat2)))


    #paillier tool
    def decrypt(self):
        _engine = self._engine
        def functor(mat):
            # _engine = RptCpuEngine(pub_key, prv_key)
            mat_enc = _engine.load(mat)
            np_vec = _engine.decrypt(mat_enc)
            print("decrypt", np_vec)
            return np_vec
        return RollPaillierTensor(self._store.map_values(lambda mat: functor(mat)))

    def out(self, str = "[CHAN ZHEN NAN]"):
        _engine = self._engine
        def seq_op(mat, str):
            #two numpy mul (l: from disk 2:from memory)
            if isinstance(mat, np.ndarray):
                print(str)
                print("[out] [numpy] : ", mat)
                #a = _engine.num2Mng_test(mat)

                return b'100'
            else:
                m = _engine.load(mat)
                print(str)
                mac = _engine.out(m)
                return b'100'
        return RollPaillierTensor(self._store.map_values(lambda v: seq_op(v, str)))


    def out2(self, str = "[CHAN ZHEN NAN]"):
       return self._store.reduce(lambda x, y : x[0][0] + y[0][0])