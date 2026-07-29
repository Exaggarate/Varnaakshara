using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using A;
using Calligrapher.ExceptionHandler;
using Calligrapher.Global;
using Calligrapher.Properties;
using FontLib;
using SLCT;
using SLGenTools.FileHandler;
using SLLangTool;

namespace Calligrapher.Language;

internal class FontHandler
{
	private Dictionary<string, string> Lookup = new Dictionary<string, string>();

	private string[] Phantoms;

	private Random r = new Random();

	public FontHandler(string script)
	{
		List<string> list = null;
		if (GObjects.LangTools != null)
		{
			while (true)
			{
				switch (4)
				{
				case 0:
					break;
				default:
					if (1 == 0)
					{
						/*OpCode not supported: LdMemberToken*/;
					}
					GObjects.LangTools.GetScriptList(new List<string> { script }, (ScriptNameType)_0019._0017(3824), ref list);
					if (list.Count == 0)
					{
						while (true)
						{
							switch (5)
							{
							case 0:
								break;
							default:
								throw new Exception(_0011._0017(8604));
							}
						}
					}
					LoadXMLData(list[_0019._0017(3828)]);
					return;
				}
			}
		}
		throw new Exception(_0011._0017(8641));
	}

	public string[] GetPhantoms()
	{
		return Phantoms;
	}

	public bool GetCharList(IFontLib slxFont, string caretChar, out List<string> charList)
	{
		List<string> list = new List<string>();
		bool result = (byte)_0019._0017(3704) != 0;
		string value = "";
		int num = Convert.ToInt32(Convert.ToChar(caretChar));
		string key = string.Format(_0011._0017(8153), num);
		int num2 = num - Convert.ToInt32(num) % _0019._0017(3708);
		if (list != null)
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
			if (slxFont != null)
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
				if (caretChar != _0011._0017(2887))
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
					if (caretChar != _0011._0017(94))
					{
						if (ContainsKey(key))
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
							TryGetValue(key, out value);
							if (value != _0011._0017(2222))
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
								num = Convert.ToInt32(Convert.ToChar(HexStringToCharString(value)));
								key = string.Format(_0011._0017(8153), num);
								num2 = num - Convert.ToInt32(num) % _0019._0017(3712);
								list = slxFont.GetGlyphCharList(num, Settings.Default.DefaultScript);
								result = (byte)_0019._0017(3716) != 0;
							}
						}
						else
						{
							list = slxFont.GetGlyphCharList(num2, Settings.Default.DefaultScript);
							result = (byte)_0019._0017(3720) != 0;
						}
						for (int i = _0019._0017(3724); i < list.Count; i += _0019._0017(3728))
						{
							list[i] = HexStringToCharString(list[i]);
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
					}
				}
				goto IL_01f0;
			}
		}
		GObjects.Log.GTLogDebugMsg(_0011._0017(8164));
		goto IL_01f0;
		IL_01f0:
		charList = list;
		return result;
	}

	public string GetCompliantString(IFontLib slxFont, string inputString)
	{
		StringBuilder stringBuilder = new StringBuilder();
		List<string> list = new List<string>();
		for (int i = _0019._0017(3732); i < inputString.Length; i += _0019._0017(3752))
		{
			char c = inputString[i];
			string value = "";
			int num = c;
			string text = string.Format(_0011._0017(8153), num);
			int num2 = num - Convert.ToInt32(num) % _0019._0017(3736);
			if (list == null)
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
			if (1 == 0)
			{
				/*OpCode not supported: LdMemberToken*/;
			}
			if (slxFont == null)
			{
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
			if (c == '\0')
			{
				continue;
			}
			if (ContainsKey(text))
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
				TryGetValue(text, out value);
				if (value != _0011._0017(2222) && text != value)
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
					num = Convert.ToInt32(Convert.ToChar(HexStringToCharString(value)));
					text = string.Format(_0011._0017(8153), num);
					list = slxFont.GetGlyphCharList(num, Settings.Default.DefaultScript);
					stringBuilder.Append(Convert.ToChar(c));
				}
				else
				{
					stringBuilder.Append(Convert.ToChar(c));
				}
				continue;
			}
			list = slxFont.GetGlyphCharList(num2, Settings.Default.DefaultScript);
			if (num % _0019._0017(3740) != 0)
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
				if (!list.Contains(string.Format(_0011._0017(8153), num)))
				{
					stringBuilder.Append(Convert.ToChar(Convert.ToInt32(_0011._0017(8241) + list[list.Count - _0019._0017(3744)], _0019._0017(3748))));
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
			}
			stringBuilder.Append(c);
		}
		while (true)
		{
			switch (4)
			{
			case 0:
				continue;
			}
			return stringBuilder.ToString();
		}
	}

	public string GetRandomChar(IFontLib slxFont, char caretChar)
	{
		List<string> charList = new List<string>();
		GetCharList(slxFont, caretChar.ToString(), out charList);
		string text = "";
		if (charList.Count == 0)
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
					return caretChar.ToString();
				}
			}
		}
		return charList[r.Next(charList.Count)];
	}

	public bool IsPhantom(string caretChar)
	{
		if (caretChar != _0011._0017(2887))
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
			string[] phantoms = GetPhantoms();
			for (int i = _0019._0017(3756); i < phantoms.Length; i += _0019._0017(3764))
			{
				string sIpString = phantoms[i];
				if (!(caretChar == HexStringToCharString(sIpString)))
				{
					continue;
				}
				while (true)
				{
					switch (7)
					{
					case 0:
						continue;
					}
					return (byte)_0019._0017(3760) != 0;
				}
			}
			while (true)
			{
				switch (1)
				{
				case 0:
					continue;
				}
				break;
			}
		}
		return (byte)_0019._0017(3768) != 0;
	}

	private string HexStringToCharString(string sIpString)
	{
		string text = null;
		if (sIpString != null)
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
			if (sIpString.Length % _0019._0017(3772) == 0)
			{
				IEnumerator<Match> enumerator = Regex.Matches(sIpString, _0011._0017(8246)).Cast<Match>().GetEnumerator();
				try
				{
					while (enumerator.MoveNext())
					{
						Match current = enumerator.Current;
						try
						{
							text += (char)Convert.ToInt32(current.Value, _0019._0017(3776));
						}
						catch (Exception)
						{
							text = null;
						}
					}
					while (true)
					{
						switch (6)
						{
						case 0:
							break;
						default:
							goto end_IL_0093;
						}
						continue;
						end_IL_0093:
						break;
					}
				}
				finally
				{
					if (enumerator != null)
					{
						while (true)
						{
							switch (4)
							{
							case 0:
								continue;
							}
							enumerator.Dispose();
							break;
						}
					}
				}
				goto IL_00b5;
			}
		}
		text = null;
		goto IL_00b5;
		IL_00b5:
		return text;
	}

	public bool ContainsKey(string key)
	{
		if (Lookup != null)
		{
			return Lookup.ContainsKey(key);
		}
		GObjects.Log.GTLogDebugMsg(_0011._0017(8255));
		return (byte)_0019._0017(3780) != 0;
	}

	public bool TryGetValue(string key, out string value)
	{
		if (Lookup != null)
		{
			while (true)
			{
				switch (7)
				{
				case 0:
					break;
				default:
					if (1 == 0)
					{
						/*OpCode not supported: LdMemberToken*/;
					}
					return Lookup.TryGetValue(key, out value);
				}
			}
		}
		value = "";
		GObjects.Log.GTLogDebugMsg(_0011._0017(8255));
		return (byte)_0019._0017(3784) != 0;
	}

	private void LoadXMLData(string script)
	{
		try
		{
			IGTFileHandler val = CES.CES0(AppPathManager.GetXMLFontCodes(script));
			if (val.GTLoadFile() == 0)
			{
				List<string> list = new List<string>();
				List<string> list2 = new List<string>();
				List<string> list3 = new List<string>();
				List<string> list4 = new List<string>();
				if (list != null)
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
					if (list2 != null)
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
						if (list3 != null)
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
							if (list4 != null)
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
								if (Lookup != null)
								{
									list.Add(_0011._0017(8425));
									list2.Add("");
									list.Add(_0011._0017(8434));
									list2.Add("");
									list.Add(_0011._0017(8445));
									list2.Add("");
									list.Add(_0011._0017(8454));
									list2.Add("");
									val.GTGetList(list, list2, (byte)_0019._0017(3788) != 0, ref list3);
									list.Remove(_0011._0017(8454));
									list.Add(_0011._0017(8463));
									val.GTGetList(list, list2, (byte)_0019._0017(3792) != 0, ref list4);
									if (list3.Count > _0019._0017(3796))
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
										if (list4.Count > _0019._0017(3800) && list3.Count == list4.Count)
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
											for (int i = _0019._0017(3804); i < list3.Count; i += _0019._0017(3808))
											{
												string key = list3[i];
												string value = list4[i];
												Lookup.Add(key, value);
											}
											while (true)
											{
												switch (2)
												{
												case 0:
													continue;
												}
												break;
											}
										}
									}
									list.Remove(_0011._0017(8463));
									list2.Remove("");
									list.Remove(_0011._0017(8445));
									list2.Remove("");
									list.Remove(_0011._0017(8434));
									list2.Remove("");
									list.Add(_0011._0017(8474));
									list2.Add("");
									list.Add(_0011._0017(8491));
									list2.Add("");
									val.GTGetList(list, list2, (byte)_0019._0017(3812) != 0, ref list4);
									Phantoms = new string[list4.Count];
									if (Phantoms != null)
									{
										while (true)
										{
											switch (1)
											{
											case 0:
												break;
											default:
											{
												for (int j = _0019._0017(3816); j < list4.Count; j += _0019._0017(3820))
												{
													string text = list4[j];
													Phantoms[j] = text;
												}
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
											}
										}
									}
									GObjects.Log.GTLogDebugMsg(_0011._0017(8506));
									return;
								}
							}
						}
					}
				}
				GObjects.Log.GTLogDebugMsg(_0011._0017(8298));
				return;
			}
			GObjects.Log.GTLogDebugMsg(_0011._0017(8553));
			throw new SLCIOException(_0011._0017(8553));
		}
		catch (SLCIOException)
		{
			throw;
		}
	}
}
