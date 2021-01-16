# Copyright 2018 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Bijective transformations."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# pylint: disable=unused-import,wildcard-import,line-too-long,g-importing-member

from tensorflow_probability.python.experimental.substrates.jax.bijectors.absolute_value import AbsoluteValue
from tensorflow_probability.python.experimental.substrates.jax.bijectors.affine import Affine
from tensorflow_probability.python.experimental.substrates.jax.bijectors.affine_linear_operator import AffineLinearOperator
from tensorflow_probability.python.experimental.substrates.jax.bijectors.affine_scalar import AffineScalar
from tensorflow_probability.python.experimental.substrates.jax.bijectors.batch_normalization import BatchNormalization
from tensorflow_probability.python.experimental.substrates.jax.bijectors.bijector import Bijector
from tensorflow_probability.python.experimental.substrates.jax.bijectors.blockwise import Blockwise
from tensorflow_probability.python.experimental.substrates.jax.bijectors.chain import Chain
from tensorflow_probability.python.experimental.substrates.jax.bijectors.cholesky_outer_product import CholeskyOuterProduct
from tensorflow_probability.python.experimental.substrates.jax.bijectors.cholesky_to_inv_cholesky import CholeskyToInvCholesky
from tensorflow_probability.python.experimental.substrates.jax.bijectors.correlation_cholesky import CorrelationCholesky
from tensorflow_probability.python.experimental.substrates.jax.bijectors.cumsum import Cumsum
from tensorflow_probability.python.experimental.substrates.jax.bijectors.discrete_cosine_transform import DiscreteCosineTransform
from tensorflow_probability.python.experimental.substrates.jax.bijectors.exp import Exp
from tensorflow_probability.python.experimental.substrates.jax.bijectors.expm1 import Expm1
from tensorflow_probability.python.experimental.substrates.jax.bijectors.fill_triangular import FillTriangular
from tensorflow_probability.python.experimental.substrates.jax.bijectors.gumbel import Gumbel
from tensorflow_probability.python.experimental.substrates.jax.bijectors.identity import Identity
from tensorflow_probability.python.experimental.substrates.jax.bijectors.inline import Inline
from tensorflow_probability.python.experimental.substrates.jax.bijectors.invert import Invert
from tensorflow_probability.python.experimental.substrates.jax.bijectors.iterated_sigmoid_centered import IteratedSigmoidCentered
from tensorflow_probability.python.experimental.substrates.jax.bijectors.kumaraswamy import Kumaraswamy
# from tensorflow_probability.python.experimental.substrates.jax.bijectors.masked_autoregressive import AutoregressiveLayer
# from tensorflow_probability.python.experimental.substrates.jax.bijectors.masked_autoregressive import AutoregressiveNetwork
# from tensorflow_probability.python.experimental.substrates.jax.bijectors.masked_autoregressive import masked_autoregressive_default_template
# from tensorflow_probability.python.experimental.substrates.jax.bijectors.masked_autoregressive import masked_dense
# from tensorflow_probability.python.experimental.substrates.jax.bijectors.masked_autoregressive import MaskedAutoregressiveFlow
from tensorflow_probability.python.experimental.substrates.jax.bijectors.matrix_inverse_tril import MatrixInverseTriL
# from tensorflow_probability.python.experimental.substrates.jax.bijectors.matveclu import MatvecLU
from tensorflow_probability.python.experimental.substrates.jax.bijectors.normal_cdf import NormalCDF
from tensorflow_probability.python.experimental.substrates.jax.bijectors.ordered import Ordered
from tensorflow_probability.python.experimental.substrates.jax.bijectors.permute import Permute
from tensorflow_probability.python.experimental.substrates.jax.bijectors.power_transform import PowerTransform
from tensorflow_probability.python.experimental.substrates.jax.bijectors.rational_quadratic_spline import RationalQuadraticSpline
# from tensorflow_probability.python.experimental.substrates.jax.bijectors.real_nvp import real_nvp_default_template
# from tensorflow_probability.python.experimental.substrates.jax.bijectors.real_nvp import RealNVP
from tensorflow_probability.python.experimental.substrates.jax.bijectors.reciprocal import Reciprocal
from tensorflow_probability.python.experimental.substrates.jax.bijectors.reshape import Reshape
from tensorflow_probability.python.experimental.substrates.jax.bijectors.scale_tril import ScaleTriL
from tensorflow_probability.python.experimental.substrates.jax.bijectors.sigmoid import Sigmoid
from tensorflow_probability.python.experimental.substrates.jax.bijectors.sinh_arcsinh import SinhArcsinh
from tensorflow_probability.python.experimental.substrates.jax.bijectors.softfloor import Softfloor
from tensorflow_probability.python.experimental.substrates.jax.bijectors.softmax_centered import SoftmaxCentered
from tensorflow_probability.python.experimental.substrates.jax.bijectors.softplus import Softplus
from tensorflow_probability.python.experimental.substrates.jax.bijectors.softsign import Softsign
from tensorflow_probability.python.experimental.substrates.jax.bijectors.square import Square
from tensorflow_probability.python.experimental.substrates.jax.bijectors.tanh import Tanh
from tensorflow_probability.python.experimental.substrates.jax.bijectors.transform_diagonal import TransformDiagonal
from tensorflow_probability.python.experimental.substrates.jax.bijectors.transpose import Transpose
from tensorflow_probability.python.experimental.substrates.jax.bijectors.weibull import Weibull

# pylint: enable=unused-import,line-too-long,g-importing-member

__all__ = [
    "AbsoluteValue",
    "Affine",
    "AffineLinearOperator",
    "AffineScalar",
    "AutoregressiveLayer",
    "AutoregressiveNetwork",
    "BatchNormalization",
    "Bijector",
    "Blockwise",
    # "CategoricalToDiscrete",  # Omitted pending further discussion.
    "Chain",
    "CholeskyOuterProduct",
    "CholeskyToInvCholesky",
    "CorrelationCholesky",
    "Cumsum",
    "DiscreteCosineTransform",
    "Exp",
    "Expm1",
    "FillTriangular",
    "Gumbel",
    "Identity",
    "Inline",
    "Invert",
    "IteratedSigmoidCentered",
    "Kumaraswamy",
    "MaskedAutoregressiveFlow",
    "MatrixInverseTriL",
    "MatvecLU",
    "NormalCDF",
    "Ordered",
    "Permute",
    "PowerTransform",
    "RationalQuadraticSpline",
    "RealNVP",
    "Reciprocal",
    "Reshape",
    "ScaleTriL",
    "Sigmoid",
    "SinhArcsinh",
    "Softfloor",
    "SoftmaxCentered",
    "Softplus",
    "Softsign",
    "Square",
    "Tanh",
    "TransformDiagonal",
    "Transpose",
    "Weibull",
    "masked_autoregressive_default_template",
    "masked_dense",
    "real_nvp_default_template"
]

