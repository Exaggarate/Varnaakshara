using System;
using System.Collections.Generic;
using System.Threading;
using A;
using FontLib.FontTables;
using FontLib.Global;

namespace FontLib.SLX.FontHandler;

public class ReadGlyph
{
	private byte[] m__001C;

	private Strokes[] m__001C;

	private GlyphTable m__001C;

	private Conversion m__001C;

	private int m__001C;

	private int m__000E;

	private int _0014;

	private double m__001C;

	private int _0018;

	private int _0007;

	private int _0001;

	private int _0002;

	private double m__000E;

	private double _0014;

	private double _0018;

	private double _0007;

	private double _0001;

	private double _0002;

	private double _001F;

	private double _0005;

	private bool m__001C;

	private bool m__000E;

	private bool _0014;

	private List<Strokes> m__001C;

	private Strokes m__001C;

	public bool CompositeGlyph => _0014;

	public List<Strokes> CompositeStrokes => this.m__001C;

	public ReadGlyph()
	{
		this.m__001C = new GlyphTable(_000F._001C(12926));
		this.m__001C = new Conversion();
		this.m__001C = (byte)_000F._001C(12930) != 0;
		_0014 = (byte)_000F._001C(12934) != 0;
		this.m__001C = new List<Strokes>();
		this.m__001C = new Strokes();
		base._002Ector();
	}

	public ReadGlyph(ReadGlyph RdGlyph)
	{
		this.m__001C = new GlyphTable(_000F._001C(12938));
		this.m__001C = new Conversion();
		this.m__001C = (byte)_000F._001C(12942) != 0;
		_0014 = (byte)_000F._001C(12946) != 0;
		this.m__001C = new List<Strokes>();
		this.m__001C = new Strokes();
		base._002Ector();
		if (RdGlyph.m__001C != null)
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
			this.m__001C = new byte[RdGlyph.m__001C.Length];
			RdGlyph.m__001C.CopyTo(this.m__001C, _000F._001C(12950));
		}
		if (RdGlyph.m__001C != null)
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
			this.m__001C = new Strokes[RdGlyph.m__001C.Length];
			RdGlyph.m__001C.CopyTo(this.m__001C, _000F._001C(12954));
		}
		if (RdGlyph.m__001C.XArray != null)
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
			this.m__001C = new GlyphTable(RdGlyph.m__001C.XArray.Length);
			RdGlyph.m__001C.XArray.CopyTo(this.m__001C.XArray, _000F._001C(12958));
			RdGlyph.m__001C.YArray.CopyTo(this.m__001C.YArray, _000F._001C(12962));
			RdGlyph.m__001C.ContBegin.CopyTo(this.m__001C.ContBegin, _000F._001C(12966));
			RdGlyph.m__001C.Flags.CopyTo(this.m__001C.Flags, _000F._001C(12970));
		}
		else
		{
			this.m__001C = new GlyphTable(_000F._001C(12974));
		}
		this.m__001C.Width = RdGlyph.m__001C.Width;
		this.m__001C.Pointer0 = RdGlyph.m__001C.Pointer0;
		this.m__001C.ReadPtr = RdGlyph.m__001C.ReadPtr;
		this.m__001C.TotalTables = RdGlyph.m__001C.TotalTables;
		this.m__001C.XMax = RdGlyph.m__001C.XMax;
		this.m__001C.XMin = RdGlyph.m__001C.XMin;
		this.m__001C.YMax = RdGlyph.m__001C.YMax;
		this.m__001C.YMin = RdGlyph.m__001C.YMin;
		this.m__001C.NoOfContours = RdGlyph.m__001C.NoOfContours;
		this.m__001C.InstCnt = RdGlyph.m__001C.InstCnt;
		this.m__001C.BezierSegCount = RdGlyph.m__001C.BezierSegCount;
		this.m__001C = new Conversion();
		this.m__001C = RdGlyph.m__001C;
		this.m__001C = RdGlyph.m__001C;
		this.m__000E = RdGlyph.m__000E;
		this._0014 = RdGlyph._0014;
		this.m__001C = RdGlyph.m__001C;
		this._0018 = RdGlyph._0018;
		this._0007 = RdGlyph._0007;
		this.m__000E = RdGlyph.m__000E;
		this._0014 = RdGlyph._0014;
		_0018 = RdGlyph._0018;
		_0007 = RdGlyph._0007;
		_0005 = RdGlyph._0005;
		_001F = RdGlyph._001F;
		_0001 = RdGlyph._0001;
		_0002 = RdGlyph._0002;
		this.m__001C = RdGlyph.m__001C;
		this.m__000E = RdGlyph.m__000E;
	}

	public void InitStringParams()
	{
		this.m__001C = (byte)_000F._001C(12382) != 0;
		_0001 = _000F._001C(12386);
		_0002 = _000F._001C(12394);
		_001F = _000F._001C(12402);
		_0005 = _000F._001C(12410);
	}

	public int GetStringHeight()
	{
		return (int)(_0002 - _0001);
	}

	public double GetStringYmax()
	{
		return _0002;
	}

	public double GetStringXmin()
	{
		return _0005;
	}

	public double GetStringXmax()
	{
		return _001F;
	}

	public int GetGlyphWidth()
	{
		return this._0018;
	}

	public void GetGlyphXBound(out double Xmax, out double Xmin)
	{
		Xmax = this._0014;
		Xmin = this.m__000E;
	}

	public int GetGlyphHeight()
	{
		return this._0007;
	}

	private byte _001C()
	{
		byte[] array = this.m__001C;
		int num = this.m__001C;
		this.m__001C = num + _000F._001C(12418);
		return array[num];
	}

	public void InitStrokes(int MaxStrokes)
	{
		this.m__001C = new Strokes[MaxStrokes];
	}

	private short _001C()
	{
		short num = _001C();
		return (short)(num + (_001C() << _000F._001C(12422)));
	}

	private void _001C(double _001C, double _000E, byte _0014, bool _0018)
	{
		try
		{
			double num = _001C + (double)this._0001;
			double num2 = _000E + (double)this._0002;
			this.m__001C.XArray[this._0014] = num;
			this.m__001C.YArray[this._0014] = num2;
			this.m__001C.Flags[this._0014] = _0014;
			this.m__001C.ContBegin[this._0014] = _0018;
			this._0014 += _000F._001C(12426);
			if (this.m__000E)
			{
				this.m__000E = num;
				this._0018 = num2;
				this._0014 = num;
				_0007 = num2;
				this.m__000E = (byte)_000F._001C(12430) != 0;
				return;
			}
			if (num < this.m__000E)
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
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				this.m__000E = num;
			}
			if (num > this._0014)
			{
				this._0014 = num;
			}
			if (num2 < this._0018)
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
				this._0018 = num2;
			}
			if (!(num2 > _0007))
			{
				return;
			}
			while (true)
			{
				switch (2)
				{
				case 0:
					continue;
				}
				_0007 = num2;
				return;
			}
		}
		catch (Exception ex)
		{
			object[] array = new object[_000F._001C(12434)];
			array[_000F._001C(12438)] = ex;
			array[_000F._001C(12442)] = _0015._001C(1028);
			array[_000F._001C(12446)] = Thread.CurrentThread.ManagedThreadId.ToString();
			array[_000F._001C(12450)] = _0015._001C(1051);
			array[_000F._001C(12454)] = this.m__001C.XArray.Length.ToString();
			array[_000F._001C(12458)] = _0015._001C(1082);
			array[_000F._001C(12462)] = this._0014.ToString();
			throw new FontException(string.Concat(array));
		}
	}

	private void _001C()
	{
		try
		{
			Strokes strokes = new Strokes();
			Strokes strokes2 = new Strokes();
			double num = _000F._001C(12466);
			double num2 = _000F._001C(12474);
			int i = _000F._001C(12482);
			if ((_0014 ? 1 : 0) == _000F._001C(12486))
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
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				this._0014 = _000F._001C(12490);
			}
			for (; i < this.m__000E; i += _000F._001C(12594))
			{
				strokes = this.m__001C[i];
				char iD = strokes.ID;
				int bezierSegCount;
				if ((uint)iD <= (uint)_000F._001C(12494))
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
					switch (iD - _000F._001C(12498))
					{
					default:
						if (iD != _000F._001C(12502))
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
						}
						else
						{
							_001C(strokes.I0 - this.m__001C, strokes.I1, (byte)_000F._001C(12530), (byte)_000F._001C(12534) != 0);
							num = strokes.I0 - this.m__001C;
							num2 = strokes.I1;
						}
						continue;
					case 0:
						this.m__001C = strokes.I5;
						continue;
					case 2:
						break;
					case 1:
						num = strokes.I0 - this.m__001C;
						num2 = strokes.I1;
						continue;
					case 3:
					{
						_001C(strokes.I0 - this.m__001C, strokes.I1, (byte)_000F._001C(12566), (byte)_000F._001C(12570) != 0);
						_001C(strokes.I2 - this.m__001C, strokes.I3, (byte)_000F._001C(12574), (byte)_000F._001C(12578) != 0);
						_001C(num, num2, (byte)_000F._001C(12582), (byte)_000F._001C(12586) != 0);
						GlyphTable glyphTable = this.m__001C;
						bezierSegCount = glyphTable.BezierSegCount;
						glyphTable.BezierSegCount = bezierSegCount + _000F._001C(12590);
						continue;
					}
					}
				}
				else
				{
					if (iD == _000F._001C(12506))
					{
						_001C(strokes.I0 - this.m__001C, strokes.I1, (byte)_000F._001C(12518), (byte)_000F._001C(12522) != 0);
						num = strokes.I0 - this.m__001C;
						num2 = strokes.I1;
						this.m__001C.NoOfContours = (short)(this.m__001C.NoOfContours + _000F._001C(12526));
						continue;
					}
					while (true)
					{
						switch (5)
						{
						case 0:
							continue;
						}
						break;
					}
					if (iD != _000F._001C(12510))
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
						if (iD != _000F._001C(12514))
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
							continue;
						}
					}
				}
				this.m__001C.SplineToBezier(num, num2, strokes, this.m__001C);
				_001C(strokes.I2 - this.m__001C, strokes.I3, (byte)_000F._001C(12538), (byte)_000F._001C(12542) != 0);
				_001C(strokes.I4 - this.m__001C, strokes.I5, (byte)_000F._001C(12546), (byte)_000F._001C(12550) != 0);
				_001C(strokes.I0 - this.m__001C, strokes.I1, (byte)_000F._001C(12554), (byte)_000F._001C(12558) != 0);
				num = strokes.I0 - this.m__001C;
				num2 = strokes.I1;
				GlyphTable glyphTable2 = this.m__001C;
				bezierSegCount = glyphTable2.BezierSegCount;
				glyphTable2.BezierSegCount = bezierSegCount + _000F._001C(12562);
			}
			while (true)
			{
				switch (4)
				{
				case 0:
					continue;
				}
				this.m__001C.Pointer0 = this._0014;
				return;
			}
		}
		catch (Exception ex)
		{
			throw new FontException(string.Concat(ex, _0015._001C(1028), Thread.CurrentThread.ManagedThreadId.ToString()));
		}
	}

	private int _001C()
	{
		try
		{
			bool flag = (byte)_000F._001C(12598) != 0;
			int num = _000F._001C(12602);
			Strokes strokes = new Strokes();
			Strokes strokes2 = new Strokes();
			while (true)
			{
				strokes = new Strokes();
				strokes.ID = Convert.ToChar(_001C());
				strokes.I0 = Convert.ToDouble(_001C());
				strokes.I1 = Convert.ToDouble(_001C());
				strokes.I2 = Convert.ToDouble(_001C());
				strokes.I3 = Convert.ToDouble(_001C());
				strokes.I4 = Convert.ToDouble(_001C());
				if (flag ? ((byte)_000F._001C(12610) != 0) : (strokes.ID == _000F._001C(12606)))
				{
					flag = (byte)_000F._001C(12614) != 0;
				}
				else
				{
					int num2;
					if (flag)
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
						if (1 == 0)
						{
							/*OpCode not supported: LdMemberToken*/;
						}
						num2 = ((strokes.ID == _000F._001C(12618)) ? 1 : 0);
					}
					else
					{
						num2 = _000F._001C(12622);
					}
					if (num2 != 0)
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
						break;
					}
				}
				char iD = strokes.ID;
				if ((uint)iD <= (uint)_000F._001C(12626))
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
					switch (iD - _000F._001C(12630))
					{
					default:
						if (iD == _000F._001C(12634))
						{
							goto IL_01f2;
						}
						while (true)
						{
							switch (7)
							{
							case 0:
								continue;
							}
							break;
						}
						goto IL_022f;
					case 0:
						num += _000F._001C(12646);
						strokes2 = strokes;
						goto IL_022f;
					case 1:
					case 11:
					case 12:
						break;
					case 2:
						goto IL_01f2;
					case 3:
						num += _000F._001C(12658);
						goto IL_022f;
					case 9:
						_0014 = (byte)_000F._001C(12662) != 0;
						this.m__001C.Add(strokes);
						goto IL_022f;
					case 4:
					case 5:
					case 6:
					case 7:
					case 8:
					case 10:
						goto IL_022f;
					}
				}
				else
				{
					if (iD == _000F._001C(12638))
					{
						goto IL_01f2;
					}
					if (iD != _000F._001C(12642))
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
						goto IL_022f;
					}
				}
				num += _000F._001C(12650);
				goto IL_022f;
				IL_022f:
				if (((strokes.ID == _000F._001C(12666)) ? 1 : 0) == _000F._001C(12670))
				{
					continue;
				}
				while (true)
				{
					switch (4)
					{
					case 0:
						continue;
					}
					break;
				}
				break;
				IL_01f2:
				num += _000F._001C(12654);
				goto IL_022f;
			}
			if (_0014)
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
				this.m__001C = strokes2;
			}
			if (strokes.ID == _000F._001C(12674))
			{
				while (true)
				{
					switch (3)
					{
					case 0:
						break;
					default:
						return (int)strokes.I0;
					}
				}
			}
			return num;
		}
		catch (Exception ex)
		{
			throw new FontException(string.Concat(ex, _0015._001C(1028), Thread.CurrentThread.ManagedThreadId.ToString()));
		}
	}

	private void _001C(int _001C)
	{
		this.m__001C = _001C;
		this.m__000E = _000F._001C(12678);
		this._0018 = _000F._001C(12682);
		this._0007 = _000F._001C(12686);
		this.m__001C.Pointer0 = _000F._001C(12690);
		this.m__001C.NoOfContours = (short)_000F._001C(12694);
	}

	private void _000E(int _001C)
	{
		this.m__001C.XArray = new double[_001C];
		this.m__001C.YArray = new double[_001C];
		this.m__001C.ContBegin = new bool[_001C];
		this.m__001C.Flags = new byte[_001C];
		this.m__001C.BezierSegCount = _000F._001C(12698);
	}

	private void _000E()
	{
		Array.Clear(this.m__001C, _000F._001C(12702), this.m__001C.Length);
		this.m__001C[this.m__000E] = new Strokes();
		this.m__001C[this.m__000E].ID = Convert.ToChar(_001C());
		this.m__001C[this.m__000E].I0 = Convert.ToDouble(_001C());
		this.m__001C[this.m__000E].I1 = Convert.ToDouble(_001C());
		this.m__001C[this.m__000E].I2 = Convert.ToDouble(_001C());
		this.m__001C[this.m__000E].I3 = Convert.ToDouble(_001C());
		this.m__001C[this.m__000E].I4 = Convert.ToDouble(_001C());
		do
		{
			this.m__000E += _000F._001C(12706);
			this.m__001C[this.m__000E] = new Strokes();
			this.m__001C[this.m__000E].ID = Convert.ToChar(_001C());
			this.m__001C[this.m__000E].I0 = Convert.ToDouble(_001C());
			this.m__001C[this.m__000E].I1 = Convert.ToDouble(_001C());
			this.m__001C[this.m__000E].I2 = Convert.ToDouble(_001C());
			this.m__001C[this.m__000E].I3 = Convert.ToDouble(_001C());
			this.m__001C[this.m__000E].I4 = Convert.ToDouble(_001C());
		}
		while (((Convert.ToChar(this.m__001C[this.m__000E].ID) == _000F._001C(12710)) ? 1 : 0) == _000F._001C(12714));
		while (true)
		{
			switch (1)
			{
			case 0:
				continue;
			}
			if (1 == 0)
			{
				/*OpCode not supported: LdMemberToken*/;
			}
			if ((this.m__000E > _000F._001C(12718)) ? ((byte)_000F._001C(12738) != 0) : (this.m__001C[_000F._001C(12722)].I1 - this.m__001C[_000F._001C(12726)].I0 == _000F._001C(12730)))
			{
				while (true)
				{
					switch (7)
					{
					case 0:
						break;
					default:
						this.m__001C.Pointer0 = _000F._001C(12742);
						return;
					}
				}
			}
			int num;
			if (this.m__000E <= _000F._001C(12746))
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
				num = ((((this.m__001C[_000F._001C(12750)].I1 - this.m__001C[_000F._001C(12754)].I0 == _000F._001C(12758)) ? 1 : 0) == _000F._001C(12766)) ? 1 : 0);
			}
			else
			{
				num = _000F._001C(12770);
			}
			if (num != 0)
			{
				this._0018 = (int)(this.m__001C[_000F._001C(12774)].I1 - this.m__001C[_000F._001C(12778)].I0);
				return;
			}
			_001C();
			if (((this.m__001C[_000F._001C(12782)].I1 - this.m__001C[_000F._001C(12786)].I0 == _000F._001C(12790)) ? 1 : 0) == _000F._001C(12798))
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
				this._0018 = (int)(this._0014 - this.m__000E);
				this._0007 = (int)(_0007 - _0018);
			}
			if (this.m__001C)
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
				_0001 = _0018;
				_0002 = _0007;
				_0005 = this.m__000E;
				_001F = this._0014;
				this.m__001C = (byte)_000F._001C(12802) != 0;
			}
			else
			{
				if (_0018 < _0001)
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
					_0001 = _0018;
				}
				if (_0007 > _0002)
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
					_0002 = _0007;
				}
				if (this.m__000E < _0005)
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
					_0005 = this.m__000E;
				}
				if (this._0014 > _001F)
				{
					_001F = this._0014;
				}
			}
			this.m__001C.XMin = (short)this.m__000E;
			this.m__001C.XMax = (short)this._0014;
			this.m__001C.YMin = (short)_0018;
			this.m__001C.YMax = (short)_0007;
			return;
		}
	}

	public GlyphTable LoadGlyph(int StartIndex, byte[] GlyphBuff)
	{
		try
		{
			this.m__000E = _000F._001C(12806);
			this._0014 = _000F._001C(12814);
			_0018 = _000F._001C(12822);
			_0007 = _000F._001C(12830);
			this._0001 = _000F._001C(12838);
			this._0002 = _000F._001C(12842);
			this.m__000E = (byte)_000F._001C(12846) != 0;
			_0014 = (byte)_000F._001C(12850) != 0;
			this.m__001C = new List<Strokes>();
			this.m__001C = new byte[GlyphBuff.Length];
			this.m__001C = GlyphBuff;
			_001C(StartIndex);
			int num = _001C();
			if (_0014)
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
						return this.m__001C;
					}
				}
			}
			_001C(StartIndex);
			_000E(num);
			_000E();
			return this.m__001C;
		}
		catch (Exception ex)
		{
			throw ex;
		}
	}

	public GlyphTable LoadCompositeGlyph(List<int> StartIndexs, byte[] GlyphBuff)
	{
		try
		{
			if (StartIndexs.Count > _000F._001C(12854))
			{
				while (true)
				{
					switch (1)
					{
					case 0:
						break;
					default:
					{
						if (1 == 0)
						{
							/*OpCode not supported: LdMemberToken*/;
						}
						this.m__000E = _000F._001C(12858);
						this._0014 = _000F._001C(12866);
						_0018 = _000F._001C(12874);
						_0007 = _000F._001C(12882);
						this.m__000E = (byte)_000F._001C(12890) != 0;
						this.m__001C = new byte[GlyphBuff.Length];
						this.m__001C = GlyphBuff;
						int num = _000F._001C(12894);
						for (int i = _000F._001C(12898); i < this.m__001C.Count; i += _000F._001C(12902))
						{
							this.m__001C = StartIndexs[i];
							num += _001C();
						}
						while (true)
						{
							switch (3)
							{
							case 0:
								break;
							default:
							{
								this._0014 = _000F._001C(12906);
								_000E(num);
								_001C(StartIndexs[_000F._001C(12910)]);
								for (int j = _000F._001C(12914); j < this.m__001C.Count; j += _000F._001C(12922))
								{
									this._0001 = (int)this.m__001C[j].I1;
									this._0002 = (int)this.m__001C[j].I2;
									this.m__001C = StartIndexs[j];
									this.m__000E = _000F._001C(12918);
									_000E();
								}
								while (true)
								{
									switch (7)
									{
									case 0:
										break;
									default:
										this._0018 = (int)(this._0014 - this.m__000E);
										this._0007 = (int)(_0007 - _0018);
										return this.m__001C;
									}
								}
							}
							}
						}
					}
					}
				}
			}
			throw new FontException(_0015._001C(1115));
		}
		catch (Exception ex)
		{
			throw ex;
		}
	}
}
