using System;
using System.Drawing;
using System.Windows;
using A;

namespace FontLib.Transformations;

public class Conversion
{
	private double _001C;

	private double _000E;

	private double _0014;

	private double _0018;

	private double _0007;

	private double _0001;

	private double _0002;

	private double _001F;

	private double _0005;

	private double _0009;

	private double _0017;

	private double _0020;

	private double _0008;

	private double _0012;

	private double _0010;

	private int[] _001C = new int[_000F._001C(7686)];

	public void CurveCoefficient(int degree)
	{
		int num = _000F._001C(6490);
		int num2 = _000F._001C(6494);
		Array.Clear(_001C, _000F._001C(6498), _001C.Length);
		for (int i = _000F._001C(6502); ((i > degree) ? 1 : 0) == _000F._001C(6526); i += _000F._001C(6522))
		{
			if (i == _000F._001C(6506))
			{
				while (true)
				{
					switch (1)
					{
					case 0:
						continue;
					}
					break;
				}
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				num = _000F._001C(6510);
			}
			else
			{
				num = num * (degree - i + _000F._001C(6514)) / i;
			}
			_001C[num2] = num;
			num2 += _000F._001C(6518);
		}
		while (true)
		{
			switch (2)
			{
			case 0:
				break;
			default:
				return;
			}
		}
	}

	public Point Spline_Point(Point[] Points, int degree, double t)
	{
		//IL_0003: Unknown result type (might be due to invalid IL or missing references)
		//IL_0118: Unknown result type (might be due to invalid IL or missing references)
		//IL_0119: Unknown result type (might be due to invalid IL or missing references)
		//IL_011c: Unknown result type (might be due to invalid IL or missing references)
		Point result = default(Point);
		((Point)(ref result)).X = _000F._001C(6530);
		((Point)(ref result)).Y = _000F._001C(6538);
		CurveCoefficient(degree);
		for (int i = _000F._001C(6546); ((i > degree) ? 1 : 0) == _000F._001C(6570); i += _000F._001C(6566))
		{
			((Point)(ref result)).X = ((Point)(ref result)).X + ((Point)(ref Points[i])).X * Math.Pow(_000F._001C(6550) - t, degree - i) * Math.Pow(t, i) * (double)_001C[i];
			((Point)(ref result)).Y = ((Point)(ref result)).Y + ((Point)(ref Points[i])).Y * Math.Pow(_000F._001C(6558) - t, degree - i) * Math.Pow(t, i) * (double)_001C[i];
		}
		while (true)
		{
			switch (6)
			{
			case 0:
				continue;
			}
			if (1 == 0)
			{
				/*OpCode not supported: LdMemberToken*/;
			}
			return result;
		}
	}

	public PointF[] BSplineCoefficient(double X0, double Y0, double X1, double Y1, double X2, double Y2)
	{
		PointF[] array = new PointF[_000F._001C(6574)];
		array[_000F._001C(6578)].X = (float)X0;
		array[_000F._001C(6582)].X = (float)(_000F._001C(6586) * (X0 - X1));
		array[_000F._001C(6594)].X = (float)(X0 - _000F._001C(6598) * X1 + X2);
		array[_000F._001C(6606)].X = _000F._001C(6610);
		array[_000F._001C(6614)].Y = (float)Y0;
		array[_000F._001C(6618)].Y = (float)(_000F._001C(6622) * (Y0 - Y1));
		array[_000F._001C(6630)].Y = (float)(Y0 - _000F._001C(6634) * Y1 + Y2);
		array[_000F._001C(6642)].Y = _000F._001C(6646);
		return array;
	}

	public PointF[] BezierCoefficient(double X0, double Y0, double X1, double Y1, double X2, double Y2, double X3, double Y3)
	{
		PointF[] array = new PointF[_000F._001C(6650)];
		array[_000F._001C(6654)].X = (float)X0;
		array[_000F._001C(6658)].X = (float)(_000F._001C(6662) * (X1 - X0));
		array[_000F._001C(6670)].X = (float)(_000F._001C(6674) * (X2 - _000F._001C(6682) * X1 + X0));
		array[_000F._001C(6690)].X = (float)(X3 - _000F._001C(6694) * X2 + _000F._001C(6702) * X1 - X0);
		array[_000F._001C(6710)].Y = (float)Y0;
		array[_000F._001C(6714)].Y = (float)(_000F._001C(6718) * (Y1 - Y0));
		array[_000F._001C(6726)].Y = (float)(_000F._001C(6730) * (Y2 - _000F._001C(6738) * Y1 + Y0));
		array[_000F._001C(6746)].Y = (float)(Y3 - _000F._001C(6750) * Y2 + _000F._001C(6758) * Y1 - Y0);
		return array;
	}

	public Point BezierPoint(double U, double X0, double Y0, double X1, double Y1, double X2, double Y2, double X3, double Y3)
	{
		//IL_014e: Unknown result type (might be due to invalid IL or missing references)
		//IL_014f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0152: Unknown result type (might be due to invalid IL or missing references)
		Point result = default(Point);
		((Point)(ref result))._002Ector(_000F._001C(6766), _000F._001C(6774));
		this._001C = X0;
		_000E = _000F._001C(6782) * (X1 - X0);
		_0014 = _000F._001C(6790) * (X2 - _000F._001C(6798) * X1 + X0);
		_0018 = X3 - _000F._001C(6806) * X2 + _000F._001C(6814) * X1 - X0;
		_0007 = Y0;
		_0001 = _000F._001C(6822) * (Y1 - Y0);
		_0002 = _000F._001C(6830) * (Y2 - _000F._001C(6838) * Y1 + Y0);
		_001F = Y3 - _000F._001C(6846) * Y2 + _000F._001C(6854) * Y1 - Y0;
		((Point)(ref result)).X = this._001C + U * (_000E + U * (_0014 + U * _0018));
		((Point)(ref result)).Y = _0007 + U * (_0001 + U * (_0002 + U * _001F));
		return result;
	}

	public Point LinePoint(float U, float X0, float Y0, float X1, float Y1)
	{
		//IL_005c: Unknown result type (might be due to invalid IL or missing references)
		//IL_005d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0060: Unknown result type (might be due to invalid IL or missing references)
		Point result = default(Point);
		((Point)(ref result))._002Ector(_000F._001C(6862), _000F._001C(6870));
		((Point)(ref result)).X = X0 * (_000F._001C(6878) - U) + X1 * U;
		((Point)(ref result)).Y = Y0 * (_000F._001C(6882) - U) + Y1 * U;
		return result;
	}

	public void BSplineToBezier(Point[] pt, double X0, double Y0, double X1, double Y1, double X2, double Y2)
	{
		PointF[] array = new PointF[_000F._001C(6886)];
		double x = X0;
		double y = Y0;
		double x2 = X1;
		double y2 = Y1;
		double x3 = X2;
		double y3 = Y2;
		array = BSplineCoefficient(x, y, x2, y2, x3, y3);
		((Point)(ref pt[_000F._001C(6890)])).X = Math.Floor((double)(array[_000F._001C(6894)].X / _000F._001C(6898)) + X0);
		((Point)(ref pt[_000F._001C(6902)])).Y = Math.Floor((double)(array[_000F._001C(6906)].Y / _000F._001C(6910)) + Y0);
		((Point)(ref pt[_000F._001C(6914)])).X = Math.Floor((double)(array[_000F._001C(6918)].X / _000F._001C(6922)) - X0 + _000F._001C(6926) * ((Point)(ref pt[_000F._001C(6934)])).X);
		((Point)(ref pt[_000F._001C(6938)])).Y = Math.Floor((double)(array[_000F._001C(6942)].Y / _000F._001C(6946)) - Y0 + _000F._001C(6950) * ((Point)(ref pt[_000F._001C(6958)])).Y);
	}

	public double GetAngle(double X0, double Y0, double X1, double Y1)
	{
		double num = X1 - X0;
		double num2 = Y1 - Y0;
		double num3;
		if (Math.Abs(num) > _000F._001C(6962))
		{
			while (true)
			{
				switch (2)
				{
				case 0:
					continue;
				}
				break;
			}
			if (1 == 0)
			{
				/*OpCode not supported: LdMemberToken*/;
			}
			num3 = Math.Atan(Math.Abs(num2 / num));
		}
		else
		{
			num3 = _000F._001C(6970);
		}
		if (((!(num >= _000F._001C(6978))) ? 1 : 0) != _000F._001C(6986))
		{
			num3 = ((((!(num2 >= _000F._001C(6998))) ? 1 : 0) != _000F._001C(7006)) ? (_000F._001C(7018) + num3) : (_000F._001C(7010) - num3));
		}
		else
		{
			while (true)
			{
				switch (5)
				{
				case 0:
					continue;
				}
				break;
			}
			if (num2 < _000F._001C(6990))
			{
				while (true)
				{
					switch (7)
					{
					case 0:
						continue;
					}
					break;
				}
				num3 = 0.0 - num3;
			}
		}
		if (num3 > _000F._001C(7026))
		{
			while (true)
			{
				switch (5)
				{
				case 0:
					continue;
				}
				break;
			}
			num3 -= _000F._001C(7034);
		}
		return num3;
	}

	public Point GetOffsetPoint(Point P1, Point P2, Point P3, double Peelthickness)
	{
		//IL_01aa: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ab: Unknown result type (might be due to invalid IL or missing references)
		//IL_03a9: Unknown result type (might be due to invalid IL or missing references)
		//IL_03a4: Unknown result type (might be due to invalid IL or missing references)
		//IL_03a5: Unknown result type (might be due to invalid IL or missing references)
		Point result = default(Point);
		((Point)(ref result))._002Ector(_000F._001C(7042), _000F._001C(7050));
		double angle = GetAngle(((Point)(ref P1)).X, ((Point)(ref P1)).Y, ((Point)(ref P2)).X, ((Point)(ref P2)).Y);
		angle += _000F._001C(7058);
		double angle2 = GetAngle(((Point)(ref P2)).X, ((Point)(ref P2)).Y, ((Point)(ref P3)).X, ((Point)(ref P3)).Y);
		angle2 += _000F._001C(7066);
		double num = ((Point)(ref P1)).X + Peelthickness * Math.Cos(angle);
		double num2 = ((Point)(ref P1)).Y + Peelthickness * Math.Sin(angle);
		double num3 = ((Point)(ref P2)).X + Peelthickness * Math.Cos(angle);
		double num4 = ((Point)(ref P2)).Y + Peelthickness * Math.Sin(angle);
		double num5 = ((Point)(ref P2)).X + Peelthickness * Math.Cos(angle2);
		double num6 = ((Point)(ref P2)).Y + Peelthickness * Math.Sin(angle2);
		double num7 = ((Point)(ref P3)).X + Peelthickness * Math.Cos(angle2);
		double num8 = ((Point)(ref P3)).Y + Peelthickness * Math.Sin(angle2);
		if (Math.Abs(angle2 - angle) < _000F._001C(7074))
		{
			while (true)
			{
				switch (1)
				{
				case 0:
					break;
				default:
					if (1 == 0)
					{
						/*OpCode not supported: LdMemberToken*/;
					}
					((Point)(ref result)).X = Math.Round(num3);
					((Point)(ref result)).Y = Math.Round(num4);
					return result;
				}
			}
		}
		if (num == num3)
		{
			while (true)
			{
				switch (1)
				{
				case 0:
					continue;
				}
				break;
			}
			if (num5 == num7)
			{
				while (true)
				{
					switch (7)
					{
					case 0:
						continue;
					}
					break;
				}
				((Point)(ref result)).X = Math.Round(num3);
				((Point)(ref result)).Y = Math.Round(num4);
			}
			else
			{
				double num9 = (num8 - num6) / (num7 - num5);
				double num10 = num6 - num9 * num5;
				((Point)(ref result)).X = Math.Round(num);
				((Point)(ref result)).Y = Math.Round(num9 * num + num10);
			}
		}
		else if (num5 == num7)
		{
			double num11 = (num4 - num2) / (num3 - num);
			double num12 = num2 - num11 * num;
			((Point)(ref result)).X = Math.Round(num5);
			((Point)(ref result)).Y = Math.Round(num11 * num5 + num12);
		}
		else if ((num4 - num2) * (num7 - num5) == (num8 - num6) * (num3 - num))
		{
			while (true)
			{
				switch (6)
				{
				case 0:
					continue;
				}
				break;
			}
			double num13 = ((Point)(ref P2)).X - ((Point)(ref P1)).X;
			double num14 = ((Point)(ref P2)).Y - ((Point)(ref P1)).Y;
			double num15 = Math.Sqrt(num13 * num13 + num14 * num14);
			num13 /= num15;
			num14 /= num15;
			((Point)(ref result)).X = ((Point)(ref P2)).X + Peelthickness * num14;
			((Point)(ref result)).Y = ((Point)(ref P2)).Y + Peelthickness * num13;
		}
		else
		{
			double num11 = (num4 - num2) / (num3 - num);
			double num12 = num2 - num11 * num;
			double num9 = (num8 - num6) / (num7 - num5);
			double num10 = num6 - num9 * num5;
			((Point)(ref result)).X = Math.Round((num12 - num10) / (num9 - num11));
			((Point)(ref result)).Y = Math.Round((num9 * num12 - num10 * num11) / (num9 - num11));
		}
		return result;
	}

	public Point LineToBSpline(int Index, double[] XArray, double[] YArray)
	{
		//IL_0003: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d5: Unknown result type (might be due to invalid IL or missing references)
		//IL_005d: Unknown result type (might be due to invalid IL or missing references)
		//IL_005e: Unknown result type (might be due to invalid IL or missing references)
		Point result = default(Point);
		((Point)(ref result)).X = _000F._001C(7082);
		((Point)(ref result)).Y = _000F._001C(7090);
		if (YArray[Index - _000F._001C(7098)] == YArray[Index])
		{
			while (true)
			{
				switch (5)
				{
				case 0:
					break;
				default:
					if (1 == 0)
					{
						/*OpCode not supported: LdMemberToken*/;
					}
					return result;
				}
			}
		}
		double num = XArray[Index - _000F._001C(7102)];
		double num2 = YArray[Index - _000F._001C(7106)];
		double num3 = XArray[Index];
		double num4 = YArray[Index];
		((Point)(ref result)).X = (int)(num + Math.Floor((num3 - num) / _000F._001C(7110)));
		((Point)(ref result)).Y = (int)(num2 + Math.Floor((num4 - num2) / _000F._001C(7118)));
		return result;
	}

	public void GetSplineCoefficient(char Id)
	{
		double num = _000F._001C(7126);
		double num2 = _000F._001C(7134);
		double num3 = _000F._001C(7142);
		double num4 = _000F._001C(7150);
		_0007 = _000F._001C(7158);
		_0001 = _000F._001C(7166);
		_0002 = _000F._001C(7174);
		_001F = _000F._001C(7182);
		this._001C = _000F._001C(7190);
		_000E = _000F._001C(7198);
		_0014 = _000F._001C(7206);
		_0018 = _000F._001C(7214);
		int num5;
		if (_0005 == _0017)
		{
			while (true)
			{
				switch (5)
				{
				case 0:
					continue;
				}
				break;
			}
			if (1 == 0)
			{
				/*OpCode not supported: LdMemberToken*/;
			}
			num5 = ((_0009 == _0020) ? 1 : 0);
		}
		else
		{
			num5 = _000F._001C(7222);
		}
		if (num5 != 0)
		{
			while (true)
			{
				switch (3)
				{
				case 0:
					break;
				default:
					return;
				}
			}
		}
		double num6 = _0005;
		double num7 = _0009;
		num = _0008;
		double num8 = _0017;
		double num9 = _0020;
		num2 = _0012;
		double num10 = _0010;
		num *= _000F._001C(7226);
		num2 *= _000F._001C(7234);
		double num11 = Math.Sqrt(Math.Pow(num8 - num6, _000F._001C(7242)) + Math.Pow(num9 - num7, _000F._001C(7250)));
		double num12 = (num8 - num6) / num11;
		double num13 = (num9 - num7) / num11;
		double num14 = Math.Cos(num);
		double num15 = Math.Sin(num);
		double num16 = num12 * num15 - num14 * num13;
		double num17;
		if (((Math.Abs(num16) == _000F._001C(7258)) ? 1 : 0) == _000F._001C(7266))
		{
			while (true)
			{
				switch (4)
				{
				case 0:
					continue;
				}
				break;
			}
			num16 /= Math.Sqrt(_000F._001C(7270) - Math.Pow(num16, _000F._001C(7278)));
			num17 = Math.Abs(Math.Atan(num16));
		}
		else
		{
			num17 = _000F._001C(7286);
		}
		num14 = Math.Cos(num2);
		num15 = Math.Sin(num2);
		num16 = num12 * num15 - num14 * num13;
		double num18;
		if (((Math.Abs(num16) == _000F._001C(7294)) ? 1 : 0) == _000F._001C(7302))
		{
			while (true)
			{
				switch (5)
				{
				case 0:
					continue;
				}
				break;
			}
			num16 /= Math.Sqrt(_000F._001C(7306) - Math.Pow(num16, _000F._001C(7314)));
			num18 = Math.Abs(Math.Atan(num16));
		}
		else
		{
			num18 = _000F._001C(7322);
		}
		char c = Id;
		if (c != _000F._001C(7330))
		{
			while (true)
			{
				switch (2)
				{
				case 0:
					continue;
				}
				break;
			}
			if (c != _000F._001C(7334))
			{
				while (true)
				{
					switch (6)
					{
					case 0:
						continue;
					}
					break;
				}
				if (c != _000F._001C(7338))
				{
					while (true)
					{
						switch (3)
						{
						case 0:
							continue;
						}
						break;
					}
				}
				else
				{
					double num19 = Math.Sin(num17 + num18);
					if (num19 == _000F._001C(7526))
					{
						while (true)
						{
							switch (4)
							{
							case 0:
								continue;
							}
							break;
						}
						num19 = _000F._001C(7534);
					}
					num3 = _000F._001C(7542) * num11 * num10 * Math.Abs(Math.Sin(num18) / num19);
					num4 = _000F._001C(7550) * num11 * num10 * Math.Abs(Math.Sin(num17) / num19);
				}
			}
			else
			{
				double num19 = (_000F._001C(7390) + Math.Cos((num17 + num18) / _000F._001C(7398))) * Math.Sin((num17 + num18) / _000F._001C(7406));
				if (num19 == _000F._001C(7414))
				{
					while (true)
					{
						switch (6)
						{
						case 0:
							continue;
						}
						break;
					}
					num19 = _000F._001C(7422);
				}
				num3 = Math.Abs(_000F._001C(7430) * num11 * Math.Sin(num18) / num19);
				num4 = Math.Abs(_000F._001C(7438) * num11 * Math.Sin(num17) / num19);
				if (((!(num3 <= _000F._001C(7446) * num11)) ? 1 : 0) == _000F._001C(7454))
				{
					while (true)
					{
						switch (5)
						{
						case 0:
							continue;
						}
						break;
					}
					num3 = _000F._001C(7458) * num11;
				}
				if (((!(num3 >= _000F._001C(7466) * num11)) ? 1 : 0) == _000F._001C(7474))
				{
					while (true)
					{
						switch (6)
						{
						case 0:
							continue;
						}
						break;
					}
					num3 = _000F._001C(7478) * num11;
				}
				if (((!(num4 <= _000F._001C(7486) * num11)) ? 1 : 0) == _000F._001C(7494))
				{
					num4 = _000F._001C(7498) * num11;
				}
				if (((!(num4 >= _000F._001C(7506) * num11)) ? 1 : 0) == _000F._001C(7514))
				{
					while (true)
					{
						switch (2)
						{
						case 0:
							continue;
						}
						break;
					}
					num4 = _000F._001C(7518) * num11;
				}
			}
		}
		else
		{
			num3 = _000F._001C(7342) * num11 / (_000F._001C(7350) + _000F._001C(7358) * Math.Cos(num18) + Math.Cos(num17));
			num4 = _000F._001C(7366) * num11 / (_000F._001C(7374) + _000F._001C(7382) * Math.Cos(num17) + Math.Cos(num18));
		}
		this._001C = (float)num6;
		_000E = (float)(num3 * Math.Cos(num));
		_0014 = (float)(_000F._001C(7558) * (num8 - num6) - num4 * Math.Cos(num2) - _000F._001C(7566) * num3 * Math.Cos(num));
		_0018 = (float)(_000F._001C(7574) * (num8 - num6) + num4 * Math.Cos(num2) + num3 * Math.Cos(num));
		_0007 = (float)num7;
		_0001 = (float)(num3 * Math.Sin(num));
		_0002 = (float)(_000F._001C(7582) * (num9 - num7) - num4 * Math.Sin(num2) - _000F._001C(7590) * num3 * Math.Sin(num));
		_001F = (float)(_000F._001C(7598) * (num9 - num7) + num4 * Math.Sin(num2) + num3 * Math.Sin(num));
	}

	public Point[] SplineToBezier(char StrokeID, double X0, double Y0, double X1, double Y1, double Theta1, double Theta2, double TensionFactor, double Offset)
	{
		Point[] array = (Point[])(object)new Point[_000F._001C(7606)];
		_0005 = X0;
		_0009 = Y0;
		_0017 = X1 - Offset;
		_0020 = Y1;
		_0008 = Theta1;
		_0012 = Theta2;
		_0010 = TensionFactor / _000F._001C(7610);
		GetSplineCoefficient(StrokeID);
		double num = _000E / _000F._001C(7618) + _0005;
		double num2 = _0001 / _000F._001C(7626) + _0009;
		double x = _0014 / _000F._001C(7634) - _0005 + _000F._001C(7642) * num;
		double y = _0002 / _000F._001C(7650) - _0009 + _000F._001C(7658) * num2;
		StrokeID = (char)_000F._001C(7666);
		((Point)(ref array[_000F._001C(7670)])).X = num;
		((Point)(ref array[_000F._001C(7674)])).Y = num2;
		((Point)(ref array[_000F._001C(7678)])).X = x;
		((Point)(ref array[_000F._001C(7682)])).Y = y;
		return array;
	}
}
