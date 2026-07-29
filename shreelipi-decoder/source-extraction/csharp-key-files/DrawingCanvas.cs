using System;
using System.Drawing;
using System.Text.RegularExpressions;
using System.Threading;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Forms;
using System.Windows.Media;
using System.Windows.Shapes;
using System.Windows.Threading;
using A;
using FontLib;
using FontLib.FontTables;
using FontLib.Transformations;
using SaveGraphics.Settings;

namespace Calligrapher.Drawing;

public abstract class DrawingCanvas : Canvas
{
	private DrawSettings settings;

	private string inputString;

	private IFontLib font;

	private GlyphTable mGlyphTable;

	private DispatcherTimer mDispatcherTimer = new DispatcherTimer();

	private Conversion mConversion = new Conversion();

	private PointCollection mPointCollection = new PointCollection();

	private int[] mLocaArray = new int[_0019._0017(5292)];

	private byte[] mBuffer = new byte[_0019._0017(5296)];

	private ushort[] mCodeArray = new ushort[_0019._0017(5300)];

	private Point[] mCoordArray = (Point[])(object)new Point[_0019._0017(5304)];

	private int[] mPointsInContour = new int[_0019._0017(5308)];

	private short[] mSampleWidths = new short[_0019._0017(5312)];

	private uint[] mSampleCodeArray = new uint[_0019._0017(5316)];

	private int[] mSampleEndPoints = new int[_0019._0017(5320)];

	private int[] mGlyphXArray = new int[_0019._0017(5324)];

	private int[] mGlyphYArray = new int[_0019._0017(5328)];

	private double mXGlyphOrigin;

	private double mYGlyphOrigin;

	private double mXStringOrigin;

	private double mYStringOrigin;

	private int mContourCnt;

	private int mPointsCnt;

	private static object thisLock = new object();

	public DrawSettings Settings
	{
		get
		{
			return settings;
		}
		set
		{
			settings = value;
		}
	}

	public string InputString
	{
		get
		{
			return inputString;
		}
		set
		{
			inputString = value;
		}
	}

	public IFontLib SLXFont
	{
		get
		{
			return font;
		}
		set
		{
			font = value;
			DrawString(_0019._0017(4516));
		}
	}

	public DrawingCanvas(DrawSettings settings, IFontLib slxFont, string inputStr)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Expected O, but got Unknown
		//IL_000c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Expected O, but got Unknown
		//IL_0017: Unknown result type (might be due to invalid IL or missing references)
		//IL_0021: Expected O, but got Unknown
		Settings = settings;
		SLXFont = slxFont;
		InputString = Regex.Replace(inputStr, _0011._0017(7324), "");
	}

	public void ClearCanvas()
	{
		((Panel)this).Children.Clear();
	}

	private bool IsOnCurve(int Index)
	{
		return (mGlyphTable.Flags[Index] & _0019._0017(4520)) == _0019._0017(4524);
	}

	private void MoveTo(Point Pnt)
	{
		((Point)(ref mCoordArray[mPointsCnt])).X = mXStringOrigin + (mXGlyphOrigin + ((Point)(ref Pnt)).X) * Settings.ZoomFactor;
		((Point)(ref mCoordArray[mPointsCnt])).Y = mYStringOrigin + mYGlyphOrigin - ((Point)(ref Pnt)).Y * Settings.ZoomFactor;
		mPointsCnt += _0019._0017(4528);
		mPointsInContour[mContourCnt] += _0019._0017(4532);
		mContourCnt += _0019._0017(4536);
	}

	private void LineTo(Point Pnt)
	{
		((Point)(ref mCoordArray[mPointsCnt])).X = mXStringOrigin + (mXGlyphOrigin + ((Point)(ref Pnt)).X) * Settings.ZoomFactor;
		((Point)(ref mCoordArray[mPointsCnt])).Y = mYStringOrigin + mYGlyphOrigin - ((Point)(ref Pnt)).Y * Settings.ZoomFactor;
		mPointsCnt += _0019._0017(4540);
		mPointsInContour[mContourCnt - _0019._0017(4544)] += _0019._0017(4548);
	}

	public void FillCharacter(bool Fillflag, Brush brush)
	{
		//IL_0027: Unknown result type (might be due to invalid IL or missing references)
		//IL_002d: Expected O, but got Unknown
		//IL_004d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0054: Expected O, but got Unknown
		//IL_0092: Unknown result type (might be due to invalid IL or missing references)
		//IL_0098: Expected O, but got Unknown
		//IL_00a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_0180: Unknown result type (might be due to invalid IL or missing references)
		//IL_0187: Expected O, but got Unknown
		//IL_00ca: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d0: Expected O, but got Unknown
		//IL_00db: Unknown result type (might be due to invalid IL or missing references)
		int i = _0019._0017(4552);
		int num = _0019._0017(4556);
		int num2 = _0019._0017(4560);
		if (Fillflag)
		{
			Path val = new Path();
			((Shape)val).Stroke = brush;
			((Shape)val).StrokeThickness = _0019._0017(4564);
			((Shape)val).Fill = brush;
			PathGeometry val2 = new PathGeometry();
			val2.FillRule = (FillRule)_0019._0017(4572);
			PathFigure[] array = (PathFigure[])(object)new PathFigure[mContourCnt];
			LineSegment[] array2 = (LineSegment[])(object)new LineSegment[mPointsCnt];
			for (num = _0019._0017(4576); num < mContourCnt; num += _0019._0017(4588))
			{
				array[num] = new PathFigure();
				array[num].StartPoint = mCoordArray[i];
				num2 = mPointsInContour[num] + num2;
				for (i += _0019._0017(4580); i < num2; i += _0019._0017(4584))
				{
					array2[i] = new LineSegment();
					array2[i].Point = mCoordArray[i];
					array[num].Segments.Add((PathSegment)(object)array2[i]);
				}
				val2.Figures.Add(array[num]);
			}
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
				val.Data = (Geometry)(object)val2;
				((Panel)this).Children.Add((UIElement)(object)val);
				return;
			}
		}
		for (num = _0019._0017(4592); num < mContourCnt; num += _0019._0017(4616))
		{
			for (num2 = mPointsInContour[num] + num2; i < num2 - _0019._0017(4612); i += _0019._0017(4608))
			{
				Line val3 = new Line();
				((Shape)val3).Stroke = (Brush)(object)Brushes.Blue;
				((DependencyObject)val3).SetValue(RenderOptions.EdgeModeProperty, (object)(EdgeMode)_0019._0017(4596));
				val3.X1 = ((Point)(ref mCoordArray[i])).X;
				val3.Y1 = ((Point)(ref mCoordArray[i])).Y;
				val3.X2 = ((Point)(ref mCoordArray[i + _0019._0017(4600)])).X;
				val3.Y2 = ((Point)(ref mCoordArray[i + _0019._0017(4604)])).Y;
				((Panel)this).Children.Add((UIElement)(object)val3);
			}
			while (true)
			{
				switch (4)
				{
				case 0:
					break;
				default:
					goto end_IL_0259;
				}
				continue;
				end_IL_0259:
				break;
			}
			i = num2;
		}
		while (true)
		{
			switch (5)
			{
			case 0:
				break;
			default:
				return;
			}
		}
	}

	private void DrawBezier(int Index)
	{
		//IL_06a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_0797: Unknown result type (might be due to invalid IL or missing references)
		_ = new Point[_0019._0017(4620)];
		PointF[] array = new PointF[_0019._0017(4624)];
		double num;
		double num2;
		if (IsOnCurve(Index - _0019._0017(4628)))
		{
			num = mGlyphTable.XArray[Index - _0019._0017(4632)];
			num2 = mGlyphTable.YArray[Index - _0019._0017(4636)];
		}
		else
		{
			num = (mGlyphTable.XArray[Index] + mGlyphTable.XArray[Index - _0019._0017(4640)]) / _0019._0017(4644);
			num2 = (mGlyphTable.YArray[Index] + mGlyphTable.YArray[Index - _0019._0017(4652)]) / _0019._0017(4656);
		}
		double num3 = mGlyphTable.XArray[Index];
		double num4 = mGlyphTable.YArray[Index];
		double num5 = mGlyphTable.XArray[Index + _0019._0017(4664)];
		double num6 = mGlyphTable.YArray[Index + _0019._0017(4668)];
		double num7;
		double num8;
		if (IsOnCurve(Index + _0019._0017(4672)))
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
			if (1 == 0)
			{
				/*OpCode not supported: LdMemberToken*/;
			}
			num7 = mGlyphTable.XArray[Index + _0019._0017(4676)];
			num8 = mGlyphTable.YArray[Index + _0019._0017(4680)];
		}
		else
		{
			num7 = (mGlyphTable.XArray[Index] + mGlyphTable.XArray[Index + _0019._0017(4684)]) / _0019._0017(4688);
			num8 = (mGlyphTable.YArray[Index] + mGlyphTable.YArray[Index + _0019._0017(4696)]) / _0019._0017(4700);
		}
		array = mConversion.BezierCoefficient(num, num2, num3, num4, num5, num6, num7, num8);
		double num9 = array[_0019._0017(4708)].X;
		double num10 = array[_0019._0017(4712)].Y;
		double num11 = _0019._0017(4716);
		double num13;
		double num14;
		double num12;
		for (num12 = _0019._0017(4724); num12 <= _0019._0017(4788); num12 += _0019._0017(4780))
		{
			num13 = (double)array[_0019._0017(4732)].X + num12 * ((double)array[_0019._0017(4736)].X + num12 * ((double)array[_0019._0017(4740)].X + num12 * (double)array[_0019._0017(4744)].X));
			num14 = (double)array[_0019._0017(4748)].Y + num12 * ((double)array[_0019._0017(4752)].Y + num12 * ((double)array[_0019._0017(4756)].Y + num12 * (double)array[_0019._0017(4760)].Y));
			num11 += Math.Sqrt(Math.Pow(num9 - num13, _0019._0017(4764)) + Math.Pow(num10 - num14, _0019._0017(4772)));
			num9 = num13;
			num10 = num14;
		}
		num13 = array[_0019._0017(4796)].X + array[_0019._0017(4800)].X + array[_0019._0017(4804)].X + array[_0019._0017(4808)].X;
		num14 = array[_0019._0017(4812)].Y + array[_0019._0017(4816)].Y + array[_0019._0017(4820)].Y + array[_0019._0017(4824)].Y;
		num11 += Math.Sqrt(Math.Pow(num9 - num13, _0019._0017(4828)) + Math.Pow(num10 - num14, _0019._0017(4836)));
		if (num11 == _0019._0017(4844))
		{
			while (true)
			{
				switch (6)
				{
				case 0:
					break;
				default:
					return;
				}
			}
		}
		double num15;
		if (num11 >= _0019._0017(4852))
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
			num15 = _0019._0017(4860) / num11;
		}
		else if (num11 >= _0019._0017(4868))
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
			num15 = _0019._0017(4876) / num11;
		}
		else
		{
			num15 = _0019._0017(4884) / num11;
		}
		num15 /= Settings.ZoomFactor;
		if (num15 > _0019._0017(4892))
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
			num15 = _0019._0017(4900);
		}
		num12 = num15;
		double num16 = _0019._0017(4908) - _0019._0017(4916) * num12;
		Point pnt = default(Point);
		((Point)(ref pnt))._002Ector(_0019._0017(4924), _0019._0017(4932));
		for (; num12 <= num16; num12 += num15)
		{
			((Point)(ref pnt)).X = (float)((double)array[_0019._0017(4940)].X + num12 * ((double)array[_0019._0017(4944)].X + num12 * ((double)array[_0019._0017(4948)].X + num12 * (double)array[_0019._0017(4952)].X)));
			((Point)(ref pnt)).Y = (float)((double)array[_0019._0017(4956)].Y + num12 * ((double)array[_0019._0017(4960)].Y + num12 * ((double)array[_0019._0017(4964)].Y + num12 * (double)array[_0019._0017(4968)].Y)));
			LineTo(pnt);
		}
		while (true)
		{
			switch (3)
			{
			case 0:
				continue;
			}
			((Point)(ref pnt)).X = array[_0019._0017(4972)].X + array[_0019._0017(4976)].X + array[_0019._0017(4980)].X + array[_0019._0017(4984)].X;
			((Point)(ref pnt)).Y = array[_0019._0017(4988)].Y + array[_0019._0017(4992)].Y + array[_0019._0017(4996)].Y + array[_0019._0017(5000)].Y;
			LineTo(pnt);
			return;
		}
	}

	private void RenderSLXChar()
	{
		//IL_0018: Unknown result type (might be due to invalid IL or missing references)
		//IL_0020: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f9: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00da: Unknown result type (might be due to invalid IL or missing references)
		bool flag = (byte)_0019._0017(5004) != 0;
		int num = _0019._0017(5008);
		Point pnt = default(Point);
		Point val = default(Point);
		int num2 = _0019._0017(5012);
		for (num2 = _0019._0017(5016); num2 <= mGlyphTable.Pointer0 - _0019._0017(5032); num2 += _0019._0017(5028))
		{
			flag = (byte)((!mGlyphTable.ContBegin[num2]) ? _0019._0017(5024) : _0019._0017(5020)) != 0;
			((Point)(ref pnt)).X = mGlyphTable.XArray[num2];
			((Point)(ref pnt)).Y = mGlyphTable.YArray[num2];
			((Point)(ref val)).X = ((Point)(ref pnt)).X;
			((Point)(ref val)).Y = ((Point)(ref pnt)).Y;
			if (IsOnCurve(num2))
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
				if (flag)
				{
					MoveTo(pnt);
				}
				else
				{
					LineTo(pnt);
				}
				continue;
			}
			if (flag)
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
				MoveTo(pnt);
				DrawBezier(num2);
			}
			else
			{
				DrawBezier(num2);
			}
			num2 += num;
		}
		while (true)
		{
			switch (6)
			{
			case 0:
				break;
			default:
				return;
			}
		}
	}

	private void DrawSlxChar(IFontLib slxFont, Brush brush)
	{
		Array.Clear(mCoordArray, _0019._0017(5036), mCoordArray.Length);
		Array.Clear(mPointsInContour, _0019._0017(5040), mPointsInContour.Length);
		mContourCnt = _0019._0017(5044);
		mPointsCnt = _0019._0017(5048);
		mGlyphTable = slxFont.GetGlyphTable();
		RenderSLXChar();
		FillCharacter(Settings.FillRule, brush);
	}

	public void DrawString(int highlight)
	{
		object obj = thisLock;
		bool lockTaken = (byte)_0019._0017(5052) != 0;
		try
		{
			Monitor.Enter(obj, ref lockTaken);
			ClearCanvas();
			try
			{
				if (InputString == null)
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
					if (1 == 0)
					{
						/*OpCode not supported: LdMemberToken*/;
					}
					if (InputString.Length <= _0019._0017(5056))
					{
						return;
					}
					while (true)
					{
						switch (3)
						{
						case 0:
							continue;
						}
						Settings = settings;
						ClearCanvas();
						double num = _0019._0017(5060);
						double num2 = _0019._0017(5068) * ((FrameworkElement)this).ActualWidth;
						double num3 = _0019._0017(5076) * ((FrameworkElement)this).ActualHeight;
						double num4 = ((FrameworkElement)this).ActualWidth - _0019._0017(5084) * num2;
						double num5 = ((FrameworkElement)this).ActualHeight - _0019._0017(5092) * num3;
						int num6 = _0019._0017(5100);
						int num7 = _0019._0017(5104);
						SLXFont.GetStringHeightWidth(InputString, ref num6, ref num7);
						double num8 = num5 / (double)num7;
						double num9 = num4 / (double)num6;
						double num10;
						if (!(num9 > num8))
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
							num10 = num9;
						}
						else
						{
							num10 = num8;
						}
						num = num10;
						double num11;
						if (!(num > _0019._0017(5108)))
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
							num11 = num;
						}
						else
						{
							num11 = _0019._0017(5116);
						}
						num = num11;
						mXStringOrigin = (num4 - (double)num6 * num) / _0019._0017(5124) + num2 / _0019._0017(5132) + num * (double)SLXFont.GetStringMinX();
						mYStringOrigin = (num5 - (double)num7 * num) / _0019._0017(5140) + num3 / _0019._0017(5148) + num * SLXFont.GetStringMaxY();
						mXGlyphOrigin = _0019._0017(5156);
						mYGlyphOrigin = _0019._0017(5164);
						Settings.ZoomFactor = num;
						for (int i = _0019._0017(5172); i < InputString.Length; i += _0019._0017(5176))
						{
							int num12 = InputString[i];
							if (SLXFont.LoadChar(num12) != 0)
							{
								continue;
							}
							while (true)
							{
								switch (3)
								{
								case 0:
									continue;
								}
								break;
							}
							if (highlight == i)
							{
								DrawSlxChar(SLXFont, (Brush)(object)Brushes.Red);
							}
							else
							{
								DrawSlxChar(SLXFont, (Brush)(object)Brushes.Black);
							}
							mXGlyphOrigin += SLXFont.GetGlyphWidth(num12);
						}
						if (!Settings.DemoVersion)
						{
							return;
						}
						while (true)
						{
							switch (6)
							{
							case 0:
								continue;
							}
							DrawWaterMark();
							return;
						}
					}
				}
			}
			catch (Exception)
			{
				throw;
			}
		}
		finally
		{
			if (lockTaken)
			{
				while (true)
				{
					switch (3)
					{
					case 0:
						continue;
					}
					Monitor.Exit(obj);
					break;
				}
			}
		}
	}

	private void DrawWaterMark()
	{
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_0006: Expected O, but got Unknown
		//IL_0055: Unknown result type (might be due to invalid IL or missing references)
		//IL_005b: Expected O, but got Unknown
		//IL_00bd: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c3: Expected O, but got Unknown
		//IL_0149: Unknown result type (might be due to invalid IL or missing references)
		//IL_014f: Expected O, but got Unknown
		//IL_017e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0183: Unknown result type (might be due to invalid IL or missing references)
		//IL_0186: Unknown result type (might be due to invalid IL or missing references)
		//IL_0188: Unknown result type (might be due to invalid IL or missing references)
		//IL_0192: Expected O, but got Unknown
		//IL_01ba: Unknown result type (might be due to invalid IL or missing references)
		//IL_01bf: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c1: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c4: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c6: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d0: Expected O, but got Unknown
		//IL_022c: Unknown result type (might be due to invalid IL or missing references)
		TextBlock val = new TextBlock();
		val.FontSize = (int)(((FrameworkElement)this).ActualHeight / _0019._0017(5180) / _0019._0017(5188));
		val.Text = _0011._0017(9728);
		Font val2 = new Font(((object)val.FontFamily).ToString(), (float)val.FontSize);
		Size size = TextRenderer.MeasureText(val.Text, val2);
		((FrameworkElement)val).Width = size.Width;
		((FrameworkElement)val).Height = size.Height;
		while ((double)size.Width > ((FrameworkElement)this).Width)
		{
			val.FontSize -= _0019._0017(5196);
			val2 = new Font(((object)val.FontFamily).ToString(), (float)val.FontSize);
			size = TextRenderer.MeasureText(val.Text, val2);
			((FrameworkElement)val).Width = size.Width;
			((FrameworkElement)val).Height = size.Height;
		}
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
			RotateTransform renderTransform = new RotateTransform(_0019._0017(5204), (double)(size.Width / _0019._0017(5212)), (double)(size.Height / _0019._0017(5216)));
			((UIElement)val).RenderTransform = (Transform)(object)renderTransform;
			Color val3 = Color.FromArgb((byte)_0019._0017(5220), (byte)_0019._0017(5224), (byte)_0019._0017(5228), (byte)_0019._0017(5232));
			val.Foreground = (Brush)new SolidColorBrush(val3);
			Color val4 = Color.FromArgb((byte)_0019._0017(5236), (byte)_0019._0017(5240), (byte)_0019._0017(5244), (byte)_0019._0017(5248));
			val.Background = (Brush)new SolidColorBrush(val4);
			val.TextAlignment = (TextAlignment)_0019._0017(5252);
			((FrameworkElement)val).Margin = new Thickness(_0019._0017(5256), ((FrameworkElement)this).ActualHeight / _0019._0017(5264) - (double)(size.Height / _0019._0017(5272)), _0019._0017(5276), _0019._0017(5284));
			((Panel)this).Children.Add((UIElement)(object)val);
			return;
		}
	}
}
