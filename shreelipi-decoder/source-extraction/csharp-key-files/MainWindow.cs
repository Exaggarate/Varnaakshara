using System;
using System.CodeDom.Compiler;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Linq.Expressions;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Markup;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Threading;
using A;
using Calligrapher.Compose;
using Calligrapher.Drawing;
using Calligrapher.Drawing.Adorners;
using Calligrapher.ExceptionHandler;
using Calligrapher.Global;
using Calligrapher.Language;
using Calligrapher.NetworkManager;
using Calligrapher.Properties;
using Calligrapher.RTFHandler;
using Calligrapher.Resources.DefaultTheme;
using FontLib;
using FontLib.Global;
using KeyboardTutor.Controls;
using Microsoft.CSharp.RuntimeBinder;
using Microsoft.Win32;
using PIKNIKN;
using SLCT;
using SLGenTools.FileHandler;
using SLGenTools.Global;
using SLGenTools.Log;
using SLLangTool;
using SaveGraphics.FileExport;
using SaveGraphics.Global;
using SaveGraphics.Settings;

namespace Calligrapher;

public class MainWindow : Window, IComponentConnector, IStyleConnector
{
	[CompilerGenerated]
	private static class _003C_003Eo__28
	{
		public static CallSite<Func<CallSite, object, object>> _003C_003Ep__0;

		public static CallSite<Func<CallSite, object, string>> _003C_003Ep__1;
	}

	[CompilerGenerated]
	private static class _003C_003Eo__35
	{
		public static CallSite<Func<CallSite, object, object>> _003C_003Ep__0;

		public static CallSite<Func<CallSite, ICompose, object, object>> _003C_003Ep__1;

		public static CallSite<Func<CallSite, object, List<string>>> _003C_003Ep__2;
	}

	[CompilerGenerated]
	private static class _003C_003Eo__68
	{
		public static CallSite<Func<CallSite, object, object>> _003C_003Ep__0;

		public static CallSite<Func<CallSite, object, string, object>> _003C_003Ep__1;

		public static CallSite<Func<CallSite, object, bool>> _003C_003Ep__2;

		public static CallSite<Func<CallSite, object, object>> _003C_003Ep__3;

		public static CallSite<Func<CallSite, object, string, object>> _003C_003Ep__4;

		public static CallSite<Func<CallSite, object, bool>> _003C_003Ep__5;

		public static CallSite<Func<CallSite, object, object>> _003C_003Ep__6;

		public static CallSite<Func<CallSite, object, string, object>> _003C_003Ep__7;

		public static CallSite<Func<CallSite, object, bool>> _003C_003Ep__8;

		public static CallSite<Func<CallSite, object, object>> _003C_003Ep__9;

		public static CallSite<Func<CallSite, object, string, object>> _003C_003Ep__10;

		public static CallSite<Func<CallSite, object, bool>> _003C_003Ep__11;

		public static CallSite<Func<CallSite, object, object>> _003C_003Ep__12;

		public static CallSite<Func<CallSite, object, string>> _003C_003Ep__13;

		public static CallSite<Func<CallSite, object, object>> _003C_003Ep__14;

		public static CallSite<Func<CallSite, object, string, object>> _003C_003Ep__15;

		public static CallSite<Func<CallSite, object, object>> _003C_003Ep__16;

		public static CallSite<Func<CallSite, object, bool>> _003C_003Ep__17;
	}

	private FontHandler FontHandler;

	private ICompose Compose;

	private List<RTFToolTip> RecentCollection;

	private bool UndoRedoActive;

	private bool IsDemo;

	private string CLFileName = "";

	private DrawSettings DrawSettings;

	private List<string> DrawCharList;

	private List<BitmapImage> DrawImageList = new List<BitmapImage>(_0019._0017(2324));

	private List<TextWithCanvas>[] TextWithCanvasList;

	private UndoRedo UndoRedo = new UndoRedo();

	private MainCanvasAdornerActions AdornerActions;

	private UpdatesManager UpdatesManager;

	private PromotionsManager PromotionsManager;

	private UserAnalyticsManager UserAnalyticsManager;

	private DispatcherTimer AutoUpdatesTimer = new DispatcherTimer();

	private DispatcherTimer LicensingTimer = new DispatcherTimer();

	private DispatcherTimer StartUpdatesTimer = new DispatcherTimer();

	private DispatcherTimer PromotionsTimer = new DispatcherTimer();

	private DispatcherTimer UserAnalyticsTimer = new DispatcherTimer();

	private DispatcherTimer PopupTimer = new DispatcherTimer();

	private List<Process> KBHelpProcesses;

	[CompilerGenerated]
	private PropertyChangedEventHandler m_PropertyChanged;

	private bool kbtutorOpen;

	private string kbtutorToolTip;

	internal MainWindow AppWindow;

	internal Grid MainGrid;

	internal DockPanel MainDockPanel;

	internal ComboBox cmb_script;

	internal ComboBox cmb_Font;

	internal ComboBox cmb_keyboard;

	internal Button btnNew;

	internal Button btnOpen;

	internal Button btnSave;

	internal Button btnExport;

	internal Button Undo;

	internal Button Redo;

	internal Button btn_Settings;

	internal ToggleButton btnTutor;

	internal Button btn_lnk;

	internal Button btn_checkupdate;

	internal ToolTip UpdatesToolTip;

	internal Button btn_Help;

	internal Button btn_About;

	internal Grid ContentGrid;

	internal DockPanel CanvasPanel;

	internal DragCanvas MainCanvas;

	internal TabControl TabPreviewRecent;

	internal TabItem t1;

	internal DockPanel t1Container;

	internal ListBox lst_Preview;

	internal TabItem t2;

	internal ToolTip t2ToolTip;

	internal Button btnClearAllQuicksave;

	internal DockPanel t2Container;

	internal ListBox lst_Recent;

	internal FloatingTouchScreenKeyboard KBTutor;

	private bool _contentLoaded;

	public List<IFontLib>[] DrawFont { get; set; }

	public bool KBTutorOpen
	{
		get
		{
			return kbtutorOpen;
		}
		set
		{
			kbtutorOpen = value;
			OnPropertyChanged(_0011._0017(2575));
		}
	}

	public string KBTutorToolTip
	{
		get
		{
			return kbtutorToolTip;
		}
		set
		{
			kbtutorToolTip = value;
			OnPropertyChanged(_0011._0017(2598));
		}
	}

	public event PropertyChangedEventHandler PropertyChanged
	{
		[CompilerGenerated]
		add
		{
			PropertyChangedEventHandler propertyChangedEventHandler = this.m_PropertyChanged;
			PropertyChangedEventHandler propertyChangedEventHandler2;
			do
			{
				propertyChangedEventHandler2 = propertyChangedEventHandler;
				PropertyChangedEventHandler value2 = (PropertyChangedEventHandler)Delegate.Combine(propertyChangedEventHandler2, value);
				propertyChangedEventHandler = Interlocked.CompareExchange(ref this.m_PropertyChanged, value2, propertyChangedEventHandler2);
			}
			while ((object)propertyChangedEventHandler != propertyChangedEventHandler2);
			while (true)
			{
				switch (5)
				{
				case 0:
					continue;
				}
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				return;
			}
		}
		[CompilerGenerated]
		remove
		{
			PropertyChangedEventHandler propertyChangedEventHandler = this.m_PropertyChanged;
			PropertyChangedEventHandler propertyChangedEventHandler2;
			do
			{
				propertyChangedEventHandler2 = propertyChangedEventHandler;
				PropertyChangedEventHandler value2 = (PropertyChangedEventHandler)Delegate.Remove(propertyChangedEventHandler2, value);
				propertyChangedEventHandler = Interlocked.CompareExchange(ref this.m_PropertyChanged, value2, propertyChangedEventHandler2);
			}
			while ((object)propertyChangedEventHandler != propertyChangedEventHandler2);
			while (true)
			{
				switch (7)
				{
				case 0:
					continue;
				}
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				return;
			}
		}
	}

	public MainWindow(string filename)
	{
		//IL_002c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0036: Expected O, but got Unknown
		//IL_0037: Unknown result type (might be due to invalid IL or missing references)
		//IL_0041: Expected O, but got Unknown
		//IL_0042: Unknown result type (might be due to invalid IL or missing references)
		//IL_004c: Expected O, but got Unknown
		//IL_004d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0057: Expected O, but got Unknown
		//IL_0058: Unknown result type (might be due to invalid IL or missing references)
		//IL_0062: Expected O, but got Unknown
		//IL_0063: Unknown result type (might be due to invalid IL or missing references)
		//IL_006d: Expected O, but got Unknown
		//IL_00bc: Unknown result type (might be due to invalid IL or missing references)
		//IL_0097: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a1: Expected O, but got Unknown
		try
		{
			AppDomain.CurrentDomain.AssemblyResolve += OnResolveAssembly;
			InitializeComponent();
			((FrameworkElement)this).Loaded += new RoutedEventHandler(MainWindow_Loaded);
			Application.Current.MainWindow = (Window)(object)this;
			CLFileName = filename;
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private static Assembly OnResolveAssembly(object sender, ResolveEventArgs args)
	{
		try
		{
			Assembly executingAssembly = Assembly.GetExecutingAssembly();
			string value = args.Name.Substring(_0019._0017(784), args.Name.IndexOf((char)_0019._0017(788))) + _0011._0017(1902);
			string[] manifestResourceNames = executingAssembly.GetManifestResourceNames();
			string text = null;
			int num = _0019._0017(792);
			while (true)
			{
				if (num <= manifestResourceNames.Count() - _0019._0017(800))
				{
					string text2 = manifestResourceNames[num];
					if (text2.EndsWith(value))
					{
						text = text2;
						break;
					}
					num += _0019._0017(796);
					continue;
				}
				while (true)
				{
					switch (6)
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
				break;
			}
			if (!string.IsNullOrWhiteSpace(text))
			{
				while (true)
				{
					switch (3)
					{
					case 0:
						break;
					default:
					{
						Stream manifestResourceStream = executingAssembly.GetManifestResourceStream(text);
						try
						{
							byte[] array = new byte[manifestResourceStream.Length];
							if (array != null)
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
								manifestResourceStream.Read(array, _0019._0017(804), array.Length);
							}
							return Assembly.Load(array);
						}
						finally
						{
							if (manifestResourceStream != null)
							{
								while (true)
								{
									switch (5)
									{
									case 0:
										break;
									default:
										((IDisposable)manifestResourceStream).Dispose();
										goto end_IL_0114;
									}
									continue;
									end_IL_0114:
									break;
								}
							}
						}
					}
					}
				}
			}
			return null;
		}
		catch (Exception)
		{
			return null;
		}
	}

	private bool AreObjectsNull()
	{
		//IL_0100: Unknown result type (might be due to invalid IL or missing references)
		//IL_0105: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ef: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f4: Unknown result type (might be due to invalid IL or missing references)
		if (FontHandler != null)
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
			if (Compose != null)
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
				if (RecentCollection != null && UpdatesManager != null && PromotionsManager != null)
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
					if (UserAnalyticsManager != null && AutoUpdatesTimer != null)
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
						if (LicensingTimer != null)
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
							if (StartUpdatesTimer != null)
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
								if (PromotionsTimer != null)
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
									if (UserAnalyticsTimer != null)
									{
										return (byte)_0019._0017(812) != 0;
									}
								}
							}
						}
					}
				}
			}
		}
		if (GObjects.Message != null)
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
			if (GObjects.Log != null)
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
				GObjects.Log.GTLogInfoMsg(Calligrapher.Properties.Resources.MsgApplicationLoadFailed);
			}
			GObjects.Message.ShowErrorSendLogs(Calligrapher.Properties.Resources.MsgApplicationLoadFailed);
		}
		else
		{
			MessageBox.Show(Calligrapher.Properties.Resources.MsgApplicationLoadFailed);
		}
		return (byte)_0019._0017(808) != 0;
	}

	private void MainWindow_Loaded(object sender, RoutedEventArgs e)
	{
		//IL_0099: Unknown result type (might be due to invalid IL or missing references)
		//IL_009f: Expected O, but got Unknown
		//IL_017d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0182: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c9: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ce: Unknown result type (might be due to invalid IL or missing references)
		//IL_0156: Unknown result type (might be due to invalid IL or missing references)
		//IL_0207: Unknown result type (might be due to invalid IL or missing references)
		//IL_0211: Expected O, but got Unknown
		//IL_02ab: Unknown result type (might be due to invalid IL or missing references)
		//IL_02b2: Expected O, but got Unknown
		//IL_05d3: Unknown result type (might be due to invalid IL or missing references)
		//IL_0664: Unknown result type (might be due to invalid IL or missing references)
		//IL_066e: Expected O, but got Unknown
		//IL_0676: Unknown result type (might be due to invalid IL or missing references)
		//IL_0680: Expected O, but got Unknown
		//IL_050f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0519: Expected O, but got Unknown
		//IL_0643: Unknown result type (might be due to invalid IL or missing references)
		//IL_0648: Unknown result type (might be due to invalid IL or missing references)
		//IL_0634: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			GObjects.Message = new MessageHandler();
			GObjects.Log = GTLogFactory.GetInstance((LogTypeEnum)_0019._0017(816), _0011._0017(1911) + Settings.Default.LogFileName, (byte)_0019._0017(820) != 0, (byte)_0019._0017(824) != 0, (byte)_0019._0017(828) != 0, _0019._0017(832));
			Directory.SetCurrentDirectory(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location));
			SLM val = new SLM(Environment.CurrentDirectory + _0011._0017(1916));
			if (val == null)
			{
				MessageBox.Show(Calligrapher.Properties.Resources.MsgApplicationLoad);
				return;
			}
			if (val.SLM1() == null)
			{
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
					MessageBox.Show(Calligrapher.Properties.Resources.MsgApplicationLoad);
					return;
				}
			}
			if (val.SLM11() == _0019._0017(836))
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
				IsDemo = (byte)_0019._0017(840) != 0;
			}
			else
			{
				IsDemo = (byte)_0019._0017(844) != 0;
			}
			string text = _0011._0017(1919);
			object obj;
			if (!IsDemo)
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
				obj = "";
			}
			else
			{
				obj = _0011._0017(1966);
			}
			new SplashScreen(text + (string?)obj + _0011._0017(1977)).Show((byte)_0019._0017(848) != 0, (byte)_0019._0017(852) != 0);
		}
		catch (Exception ex)
		{
			ShowExceptionAndExit(ex);
			((Window)this).Close();
			return;
		}
		try
		{
			if (GObjects.Log != null)
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
				GObjects.Log.GTCloseLog();
			}
			GObjects.Log = GTLogFactory.GetInstance((LogTypeEnum)_0019._0017(856), AppPathManager.GetLogFile(), (byte)_0019._0017(860) != 0, Settings.Default.VerboseLogs, (byte)_0019._0017(864) != 0, _0019._0017(868));
			GObjects.LM = new SLM(AppPathManager.GetInstallation());
			IGTFileHandler fileInstance = GTFileHandlerFactory.GetFileInstance(AppPathManager.GetData() + _0011._0017(1916) + Settings.Default.XMLLangDetails, (byte)_0019._0017(872) != 0, _0011._0017(1986), (FileTypeEnum)_0019._0017(876));
			if (fileInstance.GTLoadFile() != 0)
			{
				throw new Exception(_0011._0017(2059));
			}
			GObjects.LangTools = LTFactory.GetInstance(fileInstance);
			((Window)this).Title = GObjects.LM.SLM9();
			Imports.SetDllPathToInstallationPath();
			string text2 = "";
			string text3 = "";
			RegistryHelper val2 = new RegistryHelper(IsDemo);
			if (val2 == null)
			{
				GObjects.Log.GTLogDebugMsg(_0011._0017(2098));
			}
			PIKNIK instance = PIKNIK.GetInstance((Type)_0019._0017(880), val2.GetAppInstallPath());
			if (instance != null)
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
				if (instance.PIKNIK2())
				{
					instance.PIKNIK8((PIKNIKE)_0019._0017(884), ref text2, (byte)_0019._0017(888) != 0);
					CES.CES1(text2, ref text3);
				}
				else
				{
					GObjects.Log.GTLogDebugMsg(_0011._0017(2135));
				}
			}
			LoadMTDT();
			FillScriptDetails();
			if (((CollectionView)((ItemsControl)cmb_script).Items).Count > _0019._0017(892))
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
				if (Settings.Default.DefaultScript.Length == 0)
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
					Settings @default = Settings.Default;
					if (_003C_003Eo__28._003C_003Ep__1 == null)
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
						_003C_003Eo__28._003C_003Ep__1 = CallSite<Func<CallSite, object, string>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.Convert((CSharpBinderFlags)_0019._0017(896), typeof(string), typeof(MainWindow)));
					}
					Func<CallSite, object, string> target = _003C_003Eo__28._003C_003Ep__1.Target;
					CallSite<Func<CallSite, object, string>> _003C_003Ep__ = _003C_003Eo__28._003C_003Ep__1;
					if (_003C_003Eo__28._003C_003Ep__0 == null)
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
						int flags = _0019._0017(900);
						string name = _0011._0017(2174);
						Type? typeFromHandle = typeof(MainWindow);
						CSharpArgumentInfo[] array = new CSharpArgumentInfo[_0019._0017(904)];
						array[_0019._0017(908)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(912), null);
						_003C_003Eo__28._003C_003Ep__0 = CallSite<Func<CallSite, object, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.GetMember((CSharpBinderFlags)flags, name, typeFromHandle, array));
					}
					@default.DefaultScript = target(_003C_003Ep__, _003C_003Eo__28._003C_003Ep__0.Target(_003C_003Eo__28._003C_003Ep__0, ((ItemsControl)cmb_script).Items[_0019._0017(916)]));
					((SettingsBase)Settings.Default).Save();
				}
				((Selector)cmb_script).SelectedItem = Settings.Default.DefaultScript;
			}
			Compose = ComposeBase.GetInstance();
			if (Compose != null)
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
				if (Compose.Initialize(IsDemo) == text3)
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
					DrawSettings = new DrawSettings();
					if (DrawSettings != null)
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
						DrawSettings.SetDefaults();
						DrawSettings.FillRule = (byte)_0019._0017(920) != 0;
						DrawSettings.ZoomFactor = _0019._0017(924);
						DrawSettings.DemoVersion = IsDemo;
					}
					AdornerActions = MainCanvas.AddActions(DrawSettings);
					LoadFonts();
					FillFontDetails();
					FillKeyboardDetails();
					Compose.SetActivationKey(Settings.Default.ActivationKey);
					KBTutorToolTip = _0011._0017(2183);
					goto IL_05d9;
				}
			}
			GObjects.Message.ShowErrorSendLogs(Calligrapher.Properties.Resources.MsgLicense);
			goto IL_05d9;
			IL_05d9:
			RecentCollection = new List<RTFToolTip>();
			UpdatesManager = new UpdatesManager();
			PromotionsManager = new PromotionsManager();
			UserAnalyticsManager = new UserAnalyticsManager();
			if (AreObjectsNull())
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
				if (GObjects.Message != null)
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
					GObjects.Message.ShowErrorSendLogs(Calligrapher.Properties.Resources.MsgApplicationLoad);
				}
				else
				{
					MessageBox.Show(Calligrapher.Properties.Resources.MsgApplicationLoad);
				}
				((Window)this).Close();
			}
			LoadSettings();
			((UIElement)this).AddHandler(Keyboard.KeyDownEvent, (Delegate)new KeyEventHandler(HandleKeyDownEvent));
			CommandManager.AddPreviewExecutedHandler((UIElement)(object)this, new ExecutedRoutedEventHandler(OnPreviewExecuted));
			StartTimers();
			DoAction();
			if (((CollectionView)((ItemsControl)cmb_Font).Items).Count <= _0019._0017(932))
			{
				return;
			}
			while (true)
			{
				switch (5)
				{
				case 0:
					continue;
				}
				((Selector)cmb_Font).SelectedIndex = _0019._0017(936);
				return;
			}
		}
		catch (Exception ex2)
		{
			ShowExceptionAndExit(ex2);
			((Window)this).Close();
		}
	}

	private void LoadMTDT()
	{
		//IL_0042: Unknown result type (might be due to invalid IL or missing references)
		//IL_0047: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			GObjects.MH = DH.GetInstance();
			if (GObjects.MH != null)
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
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				GObjects.Message.ShowErrorOK(RegistryHelper.GetApplicationName((byte)_0019._0017(940) != 0), Calligrapher.Properties.Resources.MsgApplicationLoad);
				return;
			}
		}
		catch (Exception ex)
		{
			ShowExceptionAndExit(ex);
			((Window)this).Close();
		}
	}

	private void ShowExceptionAndExit(Exception ex)
	{
		//IL_0131: Unknown result type (might be due to invalid IL or missing references)
		//IL_0136: Unknown result type (might be due to invalid IL or missing references)
		//IL_0121: Unknown result type (might be due to invalid IL or missing references)
		//IL_0126: Unknown result type (might be due to invalid IL or missing references)
		if (GObjects.Log != null)
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
			if (ex.InnerException != null)
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
				GObjects.Log.GTLogException(ex.InnerException.Message);
				GObjects.Log.GTLogException(ex.InnerException.StackTrace);
			}
			else
			{
				GObjects.Log.GTLogException(ex.Message);
				GObjects.Log.GTLogException(ex.StackTrace);
			}
		}
		else
		{
			IGTLog instance = GTLogFactory.GetInstance((LogTypeEnum)_0019._0017(944), Environment.CurrentDirectory + _0011._0017(1916) + Settings.Default.LogFileName, (byte)_0019._0017(948) != 0, Settings.Default.VerboseLogs, (byte)_0019._0017(952) != 0, _0019._0017(956));
			instance.GTLogException(ex.Message);
			instance.GTLogException(ex.StackTrace);
		}
		if (GObjects.Message != null)
		{
			while (true)
			{
				switch (6)
				{
				case 0:
					break;
				default:
					GObjects.Message.ShowErrorSendLogs(Calligrapher.Properties.Resources.MsgApplicationLoad);
					return;
				}
			}
		}
		MessageBox.Show(Calligrapher.Properties.Resources.MsgApplicationLoad);
	}

	private void StartTimers()
	{
		//IL_0273: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (!IsDemo)
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
				if (Settings.Default.AutoUpdates)
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
					AutoUpdatesTimer.Interval = new TimeSpan(Settings.Default.TimerAutoUpdates / _0019._0017(960), _0019._0017(964), _0019._0017(968));
					AutoUpdatesTimer.Tick += AutoUpdatesTimer_Tick;
					AutoUpdatesTimer.Start();
				}
				if (Settings.Default.CheckUpdatesOnStart)
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
					StartUpdatesTimer.Interval = new TimeSpan(_0019._0017(972), _0019._0017(976), Settings.Default.TimerUpdatesOnStart);
					StartUpdatesTimer.Tick += StartUpdatesTimer_Tick;
					StartUpdatesTimer.Start();
				}
			}
			LicensingTimer.Interval = new TimeSpan(_0019._0017(980), Settings.Default.TimerLicensing, _0019._0017(984));
			LicensingTimer.Tick += LicensingTimer_Tick;
			LicensingTimer.Start();
			if (!Settings.Default.Promotions)
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
				PromotionsTimer.Interval = new TimeSpan(_0019._0017(988), _0019._0017(992), _0019._0017(996));
				PromotionsTimer.Tick += PromotionsTimer_Tick;
				PromotionsTimer.Start();
			}
			if (Settings.Default.UserAnalytics)
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
				UserAnalyticsTimer.Interval = new TimeSpan(_0019._0017(1000), _0019._0017(1004), _0019._0017(1008));
				UserAnalyticsTimer.Tick += UserAnalyticsTimer_Tick;
				UserAnalyticsTimer.Start();
			}
			PopupTimer.Interval = new TimeSpan(_0019._0017(1012), _0019._0017(1016), _0019._0017(1020));
			PopupTimer.Tick += PopupTimer_Tick;
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void FillScriptDetails()
	{
		//IL_021e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0223: Unknown result type (might be due to invalid IL or missing references)
		//IL_0231: Unknown result type (might be due to invalid IL or missing references)
		//IL_0236: Unknown result type (might be due to invalid IL or missing references)
		//IL_0081: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			List<string> list = new List<string>();
			if (list != null)
			{
				list = GObjects.MH.DH4();
				if (list.Count == _0019._0017(1024))
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
					if (list[_0019._0017(1028)].Equals(_0011._0017(2222)))
					{
						while (true)
						{
							switch (4)
							{
							case 0:
								break;
							default:
								GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionScriptLoad, Calligrapher.Properties.Resources.MsgScriptLoad);
								return;
							}
						}
					}
				}
				((ItemsControl)cmb_script).ItemsSource = null;
				((ItemsControl)cmb_script).DisplayMemberPath = _0011._0017(2174);
				((Selector)cmb_script).SelectedValuePath = _0011._0017(2225);
				List<object> list2 = new List<object>();
				foreach (string item in list)
				{
					if (!(item == _0011._0017(2236)))
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
						if (!(item == _0011._0017(2251)))
						{
							if (!(item == _0011._0017(2272)))
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
								if (!(item == _0011._0017(2289)))
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
									list2.Add(new
									{
										text = item,
										value = _0011._0017(2308)
									});
								}
							}
							else
							{
								list2.Add(new
								{
									text = item,
									value = _0011._0017(2305)
								});
							}
						}
						else
						{
							list2.Add(new
							{
								text = item,
								value = _0011._0017(2302)
							});
						}
					}
					else
					{
						list2.Add(new
						{
							text = item,
							value = _0011._0017(2222)
						});
					}
				}
				((ItemsControl)cmb_script).ItemsSource = list2;
			}
			else
			{
				GObjects.Log.GTLogDebugMsg(_0011._0017(2313));
			}
		}
		catch (SLCLockException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
			GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionScriptLoad, Calligrapher.Properties.Resources.MsgScriptLoad);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void LoadFonts()
	{
		//IL_0121: Unknown result type (might be due to invalid IL or missing references)
		//IL_0126: Unknown result type (might be due to invalid IL or missing references)
		//IL_050f: Unknown result type (might be due to invalid IL or missing references)
		List<string> list = GObjects.MH.DH4();
		DrawFont = new List<IFontLib>[list.Count];
		TextWithCanvasList = new List<TextWithCanvas>[list.Count];
		if (Settings.Default.KeyboardLayoutIndex != null)
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
			if (1 == 0)
			{
				/*OpCode not supported: LdMemberToken*/;
			}
			if (Settings.Default.KeyboardLayoutIndex.Count == list.Count)
			{
				goto IL_00df;
			}
		}
		Settings.Default.KeyboardLayoutIndex = new StringCollection();
		using (List<string>.Enumerator enumerator = list.GetEnumerator())
		{
			while (enumerator.MoveNext())
			{
				_ = enumerator.Current;
				Settings.Default.KeyboardLayoutIndex.Add(_0011._0017(2222));
			}
			while (true)
			{
				switch (7)
				{
				case 0:
					break;
				default:
					goto end_IL_00c5;
				}
				continue;
				end_IL_00c5:
				break;
			}
		}
		goto IL_00df;
		IL_00df:
		List<string> list2 = null;
		string text = null;
		string text2 = null;
		GObjects.LM.SLM17(ref list2);
		if (list2 == null)
		{
			return;
		}
		while (true)
		{
			switch (4)
			{
			case 0:
				continue;
			}
			if (list2.Count == 0)
			{
				while (true)
				{
					switch (2)
					{
					case 0:
						break;
					default:
						GObjects.Message.ShowErrorSendLogs(Calligrapher.Properties.Resources.MsgFontLoad);
						return;
					}
				}
			}
			for (int i = _0019._0017(1032); i < list.Count; i += _0019._0017(1156))
			{
				if (list[i].ToUpper().Contains(_0011._0017(2251)))
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
					text = _0011._0017(2358);
					text2 = _0011._0017(2371);
				}
				else if (list[i].ToUpper().Contains(_0011._0017(2272)))
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
					text = _0011._0017(2378);
					text2 = _0011._0017(2399);
				}
				else
				{
					if (list[i].ToUpper().Contains(_0011._0017(2289)))
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
					if (list[i].ToUpper().Contains(_0011._0017(2236)))
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
						text = _0011._0017(2378);
						text2 = _0011._0017(2406);
					}
				}
				List<string> list3 = GObjects.MH.DH3(list[i], text);
				DrawFont[i] = new List<IFontLib>(list3.Count);
				TextWithCanvasList[i] = new List<TextWithCanvas>(list3.Count);
				int num = _0019._0017(1036);
				int num2 = _0019._0017(1040);
				GObjects.LM.SLM24(ref num, ref num2);
				int num3 = GObjects.LM.SLM10();
				FactoryFontLib.AdvancedFontInfo((FontLayout)_0019._0017(1044), num3, num, num2, Environment.CurrentDirectory + _0011._0017(1916));
				string bin = AppPathManager.GetBin();
				int num4 = _0019._0017(1048);
				while (true)
				{
					if (num4 < list3.Count)
					{
						string[] array = new string[_0019._0017(1052)];
						array[_0019._0017(1056)] = bin;
						array[_0019._0017(1060)] = _0011._0017(2413);
						array[_0019._0017(1064)] = text2;
						array[_0019._0017(1068)] = _0011._0017(2430);
						array[_0019._0017(1072)] = list3[num4];
						string text3 = string.Concat(array);
						string fileNameWithoutExtension = Path.GetFileNameWithoutExtension(text3);
						if (File.Exists(text3))
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
							try
							{
								IFontLib instance = FactoryFontLib.GetInstance(text3, (FontLayout)_0019._0017(1076));
								if (instance != null)
								{
									while (true)
									{
										switch (5)
										{
										case 0:
											continue;
										}
										string fontStamp = instance.GetFontStamp();
										if (GObjects.LM.SLM15(fontStamp, fileNameWithoutExtension) != GObjects.LM.SLM10())
										{
											break;
										}
										List<CanvasObject> list4 = new List<CanvasObject>();
										string text4 = "";
										if (list[i].ToUpper().Contains(_0011._0017(2251)))
										{
											text4 = Calligrapher.Properties.Resources.SampleDevString;
										}
										else if (list[i].ToUpper().Contains(_0011._0017(2272)))
										{
											text4 = Calligrapher.Properties.Resources.SampleGujString;
										}
										else if (list[i].ToUpper().Contains(_0011._0017(2289)))
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
											text4 = Calligrapher.Properties.Resources.SampleGujString;
										}
										else if (list[i].ToUpper().Contains(_0011._0017(2236)))
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
											text4 = _0011._0017(2433);
										}
										list4.Add(CanvasObject.GetObject(text4, instance, new Rect(_0019._0017(1080), _0019._0017(1088), _0019._0017(1096), _0019._0017(1104)), DrawSettings));
										IFileExport instance2 = FileExportFactory.GetInstance((FileTypes)_0019._0017(1112), "", list4, (byte)_0019._0017(1116) != 0);
										if (instance2 != null)
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
											instance2.SetDimension(_0019._0017(1120), _0019._0017(1124));
											instance2.SetBackground((BackGround)_0019._0017(1128), _0011._0017(278));
											instance2.SetDpi(_0019._0017(1132), _0019._0017(1140));
											instance2.SetFontColorSpace((ColorSpace)_0019._0017(1148), _0011._0017(278));
											Bitmap val = instance2.ExportImage();
											TextWithCanvasList[i].Add(new TextWithCanvas(instance.GetFontName(), BitmapConversion.ToBitmapImage(val)));
										}
										DrawFont[i].Add(instance);
										if (!IsDemo)
										{
											break;
										}
										while (true)
										{
											switch (5)
											{
											case 0:
												break;
											default:
												goto end_IL_0611;
											}
											continue;
											end_IL_0611:
											break;
										}
										goto end_IL_064b;
									}
								}
							}
							catch (Exception ex)
							{
								throw new Exception(ex.Message + _0011._0017(94) + text3);
							}
						}
						num4 += _0019._0017(1152);
						continue;
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
					break;
					continue;
					end_IL_064b:
					break;
				}
			}
			return;
		}
	}

	private void FillFontDetails()
	{
		//IL_0084: Unknown result type (might be due to invalid IL or missing references)
		//IL_0089: Unknown result type (might be due to invalid IL or missing references)
		//IL_0095: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			((ItemsControl)cmb_Font).ItemsSource = null;
			if (((Selector)cmb_script).SelectedIndex == _0019._0017(1160))
			{
				((Selector)cmb_script).SelectedIndex = _0019._0017(1164);
			}
			((ItemsControl)cmb_Font).ItemsSource = TextWithCanvasList[((Selector)cmb_script).SelectedIndex];
			((Selector)cmb_Font).SelectedIndex = _0019._0017(1168);
		}
		catch (SLCLockException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
			GObjects.Message.ShowErrorSendLogs(Calligrapher.Properties.Resources.MsgFontLoad);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void FillKeyboardDetails()
	{
		//IL_0293: Unknown result type (might be due to invalid IL or missing references)
		//IL_0298: Unknown result type (might be due to invalid IL or missing references)
		//IL_02a6: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ab: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d2: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d7: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (Compose == null)
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
						return;
					}
				}
			}
			if (_003C_003Eo__35._003C_003Ep__2 == null)
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
				_003C_003Eo__35._003C_003Ep__2 = CallSite<Func<CallSite, object, List<string>>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.Convert((CSharpBinderFlags)_0019._0017(1172), typeof(List<string>), typeof(MainWindow)));
			}
			Func<CallSite, object, List<string>> target = _003C_003Eo__35._003C_003Ep__2.Target;
			CallSite<Func<CallSite, object, List<string>>> _003C_003Ep__ = _003C_003Eo__35._003C_003Ep__2;
			if (_003C_003Eo__35._003C_003Ep__1 == null)
			{
				int flags = _0019._0017(1176);
				string name = _0011._0017(2448);
				Type? typeFromHandle = typeof(MainWindow);
				CSharpArgumentInfo[] array = new CSharpArgumentInfo[_0019._0017(1180)];
				array[_0019._0017(1184)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1188), null);
				array[_0019._0017(1192)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1196), null);
				_003C_003Eo__35._003C_003Ep__1 = CallSite<Func<CallSite, ICompose, object, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.InvokeMember((CSharpBinderFlags)flags, name, null, typeFromHandle, array));
			}
			Func<CallSite, ICompose, object, object> target2 = _003C_003Eo__35._003C_003Ep__1.Target;
			CallSite<Func<CallSite, ICompose, object, object>> _003C_003Ep__2 = _003C_003Eo__35._003C_003Ep__1;
			ICompose compose = Compose;
			if (_003C_003Eo__35._003C_003Ep__0 == null)
			{
				int flags2 = _0019._0017(1200);
				string name2 = _0011._0017(2225);
				Type? typeFromHandle2 = typeof(MainWindow);
				CSharpArgumentInfo[] array2 = new CSharpArgumentInfo[_0019._0017(1204)];
				array2[_0019._0017(1208)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1212), null);
				_003C_003Eo__35._003C_003Ep__0 = CallSite<Func<CallSite, object, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.GetMember((CSharpBinderFlags)flags2, name2, typeFromHandle2, array2));
			}
			List<string> list = target(_003C_003Ep__, target2(_003C_003Ep__2, compose, _003C_003Eo__35._003C_003Ep__0.Target(_003C_003Eo__35._003C_003Ep__0, ((Selector)cmb_script).SelectedItem)));
			if (list != null)
			{
				if (list.Count == 0)
				{
					while (true)
					{
						switch (6)
						{
						case 0:
							continue;
						}
						GObjects.Message.ShowErrorSendLogs(Calligrapher.Properties.Resources.MsgKeyboardLayout);
						return;
					}
				}
				((ItemsControl)cmb_keyboard).Items.Clear();
				foreach (string item in list)
				{
					((ItemsControl)cmb_keyboard).Items.Add((object)item);
				}
			}
			else
			{
				GObjects.Log.GTLogDebugMsg(_0011._0017(2479));
			}
			((Selector)cmb_keyboard).SelectedIndex = Convert.ToInt32(Settings.Default.KeyboardLayoutIndex[((Selector)cmb_script).SelectedIndex]);
		}
		catch (SLCLockException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
			GObjects.Message.ShowErrorSendLogs(Calligrapher.Properties.Resources.MsgKeyboardLayout);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void btnNew_Click(object sender, RoutedEventArgs e)
	{
		//IL_0070: Unknown result type (might be due to invalid IL or missing references)
		//IL_0075: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			((Panel)MainCanvas).Children.Clear();
			MainCanvasAdornerActions canvasAdornerActionsObject = MainCanvas.GetCanvasAdornerActionsObject();
			if (canvasAdornerActionsObject != null)
			{
				_ = MainCanvas.ElementSelected;
				canvasAdornerActionsObject.AddCanvasObject_MouseUp(null, null);
			}
			UpdatePreviewList((byte)_0019._0017(1216) != 0, null);
			EnableDisableSaveButtons();
		}
		catch (Exception ex)
		{
			GObjects.Log.GTLogException(ex);
			GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionRTBNew, Calligrapher.Properties.Resources.MsgRTBNew);
		}
	}

	private void btnOpen_Click(object sender, RoutedEventArgs e)
	{
		//IL_0057: Unknown result type (might be due to invalid IL or missing references)
		//IL_005c: Unknown result type (might be due to invalid IL or missing references)
		//IL_002f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0034: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (OpenFile())
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
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionRTBOpen, Calligrapher.Properties.Resources.MsgRTBOpen);
				return;
			}
		}
		catch (Exception ex)
		{
			GObjects.Log.GTLogException(ex);
			GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionRTBOpen, Calligrapher.Properties.Resources.MsgRTBOpen);
		}
	}

	private void btn_Settings_Click(object sender, RoutedEventArgs e)
	{
		//IL_005c: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			SettingsWindow settingsWindow = new SettingsWindow();
			if (settingsWindow != null)
			{
				while (true)
				{
					switch (6)
					{
					case 0:
						break;
					default:
						if (1 == 0)
						{
							/*OpCode not supported: LdMemberToken*/;
						}
						((Window)settingsWindow).Owner = (Window)(object)this;
						((Window)settingsWindow).ShowDialog();
						return;
					}
				}
			}
			GObjects.Log.GTLogDebugMsg(_0011._0017(2528));
		}
		catch (Exception ex)
		{
			GObjects.Log.GTLogException(ex);
			GObjects.Message.ShowErrorSendLogs(Calligrapher.Properties.Resources.MsgSettings);
		}
	}

	private void btn_Help_Click(object sender, RoutedEventArgs e)
	{
		//IL_0042: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (IsDemo)
			{
				while (true)
				{
					switch (3)
					{
					case 0:
						break;
					default:
						if (1 == 0)
						{
							/*OpCode not supported: LdMemberToken*/;
						}
						Process.Start(Calligrapher.Properties.Resources.URLYouTubeHelpDemo);
						return;
					}
				}
			}
			Process.Start(Calligrapher.Properties.Resources.URLYouTubeHelpMain);
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void btn_About_Click(object sender, RoutedEventArgs e)
	{
		//IL_004d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0052: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			AboutWindow aboutWindow = new AboutWindow();
			if (aboutWindow != null)
			{
				while (true)
				{
					switch (2)
					{
					case 0:
						break;
					default:
						if (1 == 0)
						{
							/*OpCode not supported: LdMemberToken*/;
						}
						((Window)aboutWindow).Owner = (Window)(object)this;
						((Window)aboutWindow).ShowDialog();
						return;
					}
				}
			}
			GObjects.Log.GTLogDebugMsg(_0011._0017(237));
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void btnTutor_Click(object sender, RoutedEventArgs e)
	{
		try
		{
			KeyboardTutorClick();
		}
		catch (Exception ex)
		{
			GObjects.Log.GTLogException(ex);
		}
	}

	public void OnPropertyChanged(string name)
	{
		PropertyChangedEventHandler propertyChanged = this.PropertyChanged;
		if (propertyChanged == null)
		{
			return;
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
			propertyChanged(this, new PropertyChangedEventArgs(name));
			return;
		}
	}

	public void StoreKBHelpProcess(Process p)
	{
		if (KBHelpProcesses == null)
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
			KBHelpProcesses = new List<Process>();
		}
		KBHelpProcesses.Add(p);
	}

	private void KeyboardTutorClick()
	{
		try
		{
			if (KBTutor == null)
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
				((Popup)KBTutor).IsOpen = (((Popup)KBTutor).IsOpen ? 1 : 0) == _0019._0017(1220);
				if (((Popup)KBTutor).IsOpen)
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
					KBTutorToolTip = _0011._0017(2627);
				}
				else
				{
					KBTutorToolTip = _0011._0017(2183);
				}
				KBTutorOpen = ((Popup)KBTutor).IsOpen;
				ChangeKeyboardTutorLayout();
				return;
			}
		}
		catch (Exception ex)
		{
			GObjects.Log.GTLogException(ex);
		}
	}

	private void ChangeKeyboardTutorLayout()
	{
		//IL_01ea: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ef: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (KBTutor == null || !((Popup)KBTutor).IsOpen)
			{
				return;
			}
			while (true)
			{
				switch (7)
				{
				case 0:
					continue;
				}
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				string text = null;
				string text2 = null;
				string path = null;
				if (Settings.Default.DefaultScript.ToUpper().Contains(_0011._0017(2302)))
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
					path = _0011._0017(2666);
					text2 = _0011._0017(2371);
					text = _0011._0017(2691);
				}
				else if (Settings.Default.DefaultScript.ToUpper().Contains(_0011._0017(2305)))
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
					path = _0011._0017(2722);
					text2 = _0011._0017(2399);
					text = _0011._0017(2747);
				}
				else
				{
					text2 = _0011._0017(2406);
				}
				if (text == null)
				{
					text = _0011._0017(2778);
				}
				KBTutor.LoadKeyboardTutor(Path.Combine(Environment.CurrentDirectory, path), Path.Combine(Environment.CurrentDirectory, ((Selector)cmb_keyboard).SelectedItem.ToString().ToUpper()) + _0011._0017(452) + text2, text, Path.Combine(AppPathManager.GetData(), text2, ((Selector)cmb_keyboard).SelectedItem.ToString().ToUpper() + text2 + _0011._0017(2789)), (byte)_0019._0017(1224) != 0, Convert.ToByte(_0019._0017(1228)), Convert.ToByte(_0019._0017(1232)), GetVirtualKeyCode(_0011._0017(2798)), (Action<Process>)StoreKBHelpProcess, (Action)KeyboardTutorClick);
				return;
			}
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private byte GetVirtualKeyCode(string key)
	{
		//IL_001b: Unknown result type (might be due to invalid IL or missing references)
		return Convert.ToByte(KeyInterop.VirtualKeyFromKey((Key)TypeDescriptor.GetConverter(typeof(Key)).ConvertFromString(key)));
	}

	private void OnPreviewExecuted(object sender, ExecutedRoutedEventArgs e)
	{
		//IL_001d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0022: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			((RoutedEventArgs)e).Handled = HandlePreviewExecutedCommand(e.Command);
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void btn_lnk_Click(object sender, RoutedEventArgs e)
	{
		//IL_0016: Unknown result type (might be due to invalid IL or missing references)
		//IL_001b: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			Process.Start(Calligrapher.Properties.Resources.URLStore);
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void lst_Preview_MouseDoubleClick(object sender, MouseButtonEventArgs e)
	{
		//IL_0027: Unknown result type (might be due to invalid IL or missing references)
		//IL_002c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0038: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			ReplaceWordFromList(sender);
		}
		catch (SLCCompositionException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
			GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionReplaceFromPreview, Calligrapher.Properties.Resources.MsgReplaceFromPreview);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void lst_Preview_SelectionChanged(object sender, SelectionChangedEventArgs e)
	{
		//IL_0031: Unknown result type (might be due to invalid IL or missing references)
		//IL_0040: Unknown result type (might be due to invalid IL or missing references)
		//IL_0045: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (lst_Preview != null)
			{
				ReplaceWordFromList(sender);
			}
		}
		catch (SLCCompositionException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
			GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionReplaceFromPreview, Calligrapher.Properties.Resources.MsgReplaceFromPreview);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void btnSave_Click(object sender, RoutedEventArgs e)
	{
		//IL_000f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0014: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			SaveRecentText();
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void btnExport_Click(object sender, RoutedEventArgs e)
	{
		//IL_000f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0014: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			SaveAs();
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void Undo_Click(object sender, RoutedEventArgs e)
	{
		//IL_000f: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			UndoAction();
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void Redo_Click(object sender, RoutedEventArgs e)
	{
		//IL_000f: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			RedoAction();
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void btn_checkupdate_Click(object sender, RoutedEventArgs e)
	{
		//IL_004e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0020: Unknown result type (might be due to invalid IL or missing references)
		//IL_0025: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (IsDemo)
			{
				while (true)
				{
					switch (6)
					{
					case 0:
						break;
					default:
						if (1 == 0)
						{
							/*OpCode not supported: LdMemberToken*/;
						}
						GObjects.Message.ShowErrorDemoVersion();
						return;
					}
				}
			}
			UpdatesNotification((byte)_0019._0017(1236) != 0);
			UpdatesManager.CheckUpdates();
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void cmb_script_SelectionChanged(object sender, SelectionChangedEventArgs e)
	{
		//IL_0c33: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c38: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c44: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c49: Unknown result type (might be due to invalid IL or missing references)
		//IL_099d: Unknown result type (might be due to invalid IL or missing references)
		//IL_09a7: Expected O, but got Unknown
		try
		{
			if (cmb_script == null)
			{
				return;
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
				((UIElement)cmb_keyboard).IsEnabled = (byte)_0019._0017(1240) != 0;
				((UIElement)btnTutor).IsEnabled = (byte)_0019._0017(1244) != 0;
				MainCanvas.RemoveSelection();
				if (_003C_003Eo__68._003C_003Ep__2 == null)
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
					int flags = _0019._0017(1248);
					int operation = _0019._0017(1252);
					Type? typeFromHandle = typeof(MainWindow);
					CSharpArgumentInfo[] array = new CSharpArgumentInfo[_0019._0017(1256)];
					array[_0019._0017(1260)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1264), null);
					_003C_003Eo__68._003C_003Ep__2 = CallSite<Func<CallSite, object, bool>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.UnaryOperation((CSharpBinderFlags)flags, (ExpressionType)operation, typeFromHandle, array));
				}
				Func<CallSite, object, bool> target = _003C_003Eo__68._003C_003Ep__2.Target;
				CallSite<Func<CallSite, object, bool>> _003C_003Ep__ = _003C_003Eo__68._003C_003Ep__2;
				if (_003C_003Eo__68._003C_003Ep__1 == null)
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
					int flags2 = _0019._0017(1268);
					string name = _0011._0017(2809);
					Type? typeFromHandle2 = typeof(MainWindow);
					CSharpArgumentInfo[] array2 = new CSharpArgumentInfo[_0019._0017(1272)];
					array2[_0019._0017(1276)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1280), null);
					array2[_0019._0017(1284)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1288), null);
					_003C_003Eo__68._003C_003Ep__1 = CallSite<Func<CallSite, object, string, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.InvokeMember((CSharpBinderFlags)flags2, name, null, typeFromHandle2, array2));
				}
				Func<CallSite, object, string, object> target2 = _003C_003Eo__68._003C_003Ep__1.Target;
				CallSite<Func<CallSite, object, string, object>> _003C_003Ep__2 = _003C_003Eo__68._003C_003Ep__1;
				if (_003C_003Eo__68._003C_003Ep__0 == null)
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
					int flags3 = _0019._0017(1292);
					string name2 = _0011._0017(2225);
					Type? typeFromHandle3 = typeof(MainWindow);
					CSharpArgumentInfo[] array3 = new CSharpArgumentInfo[_0019._0017(1296)];
					array3[_0019._0017(1300)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1304), null);
					_003C_003Eo__68._003C_003Ep__0 = CallSite<Func<CallSite, object, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.GetMember((CSharpBinderFlags)flags3, name2, typeFromHandle3, array3));
				}
				if (target(_003C_003Ep__, target2(_003C_003Ep__2, _003C_003Eo__68._003C_003Ep__0.Target(_003C_003Eo__68._003C_003Ep__0, ((Selector)cmb_script).SelectedItem), _0011._0017(2302))))
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
					Settings.Default.DefaultFontFamily = Settings.Default.DefaultDevFont;
				}
				else
				{
					if (_003C_003Eo__68._003C_003Ep__5 == null)
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
						int flags4 = _0019._0017(1308);
						int operation2 = _0019._0017(1312);
						Type? typeFromHandle4 = typeof(MainWindow);
						CSharpArgumentInfo[] array4 = new CSharpArgumentInfo[_0019._0017(1316)];
						array4[_0019._0017(1320)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1324), null);
						_003C_003Eo__68._003C_003Ep__5 = CallSite<Func<CallSite, object, bool>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.UnaryOperation((CSharpBinderFlags)flags4, (ExpressionType)operation2, typeFromHandle4, array4));
					}
					Func<CallSite, object, bool> target3 = _003C_003Eo__68._003C_003Ep__5.Target;
					CallSite<Func<CallSite, object, bool>> _003C_003Ep__3 = _003C_003Eo__68._003C_003Ep__5;
					if (_003C_003Eo__68._003C_003Ep__4 == null)
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
						int flags5 = _0019._0017(1328);
						string name3 = _0011._0017(2809);
						Type? typeFromHandle5 = typeof(MainWindow);
						CSharpArgumentInfo[] array5 = new CSharpArgumentInfo[_0019._0017(1332)];
						array5[_0019._0017(1336)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1340), null);
						array5[_0019._0017(1344)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1348), null);
						_003C_003Eo__68._003C_003Ep__4 = CallSite<Func<CallSite, object, string, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.InvokeMember((CSharpBinderFlags)flags5, name3, null, typeFromHandle5, array5));
					}
					Func<CallSite, object, string, object> target4 = _003C_003Eo__68._003C_003Ep__4.Target;
					CallSite<Func<CallSite, object, string, object>> _003C_003Ep__4 = _003C_003Eo__68._003C_003Ep__4;
					if (_003C_003Eo__68._003C_003Ep__3 == null)
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
						int flags6 = _0019._0017(1352);
						string name4 = _0011._0017(2225);
						Type? typeFromHandle6 = typeof(MainWindow);
						CSharpArgumentInfo[] array6 = new CSharpArgumentInfo[_0019._0017(1356)];
						array6[_0019._0017(1360)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1364), null);
						_003C_003Eo__68._003C_003Ep__3 = CallSite<Func<CallSite, object, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.GetMember((CSharpBinderFlags)flags6, name4, typeFromHandle6, array6));
					}
					if (target3(_003C_003Ep__3, target4(_003C_003Ep__4, _003C_003Eo__68._003C_003Ep__3.Target(_003C_003Eo__68._003C_003Ep__3, ((Selector)cmb_script).SelectedItem), _0011._0017(2305))))
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
						Settings.Default.DefaultFontFamily = Settings.Default.DefaultGujFont;
					}
					else
					{
						if (_003C_003Eo__68._003C_003Ep__8 == null)
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
							int flags7 = _0019._0017(1368);
							int operation3 = _0019._0017(1372);
							Type? typeFromHandle7 = typeof(MainWindow);
							CSharpArgumentInfo[] array7 = new CSharpArgumentInfo[_0019._0017(1376)];
							array7[_0019._0017(1380)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1384), null);
							_003C_003Eo__68._003C_003Ep__8 = CallSite<Func<CallSite, object, bool>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.UnaryOperation((CSharpBinderFlags)flags7, (ExpressionType)operation3, typeFromHandle7, array7));
						}
						Func<CallSite, object, bool> target5 = _003C_003Eo__68._003C_003Ep__8.Target;
						CallSite<Func<CallSite, object, bool>> _003C_003Ep__5 = _003C_003Eo__68._003C_003Ep__8;
						if (_003C_003Eo__68._003C_003Ep__7 == null)
						{
							int flags8 = _0019._0017(1388);
							string name5 = _0011._0017(2809);
							Type? typeFromHandle8 = typeof(MainWindow);
							CSharpArgumentInfo[] array8 = new CSharpArgumentInfo[_0019._0017(1392)];
							array8[_0019._0017(1396)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1400), null);
							array8[_0019._0017(1404)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1408), null);
							_003C_003Eo__68._003C_003Ep__7 = CallSite<Func<CallSite, object, string, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.InvokeMember((CSharpBinderFlags)flags8, name5, null, typeFromHandle8, array8));
						}
						Func<CallSite, object, string, object> target6 = _003C_003Eo__68._003C_003Ep__7.Target;
						CallSite<Func<CallSite, object, string, object>> _003C_003Ep__6 = _003C_003Eo__68._003C_003Ep__7;
						if (_003C_003Eo__68._003C_003Ep__6 == null)
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
							int flags9 = _0019._0017(1412);
							string name6 = _0011._0017(2225);
							Type? typeFromHandle9 = typeof(MainWindow);
							CSharpArgumentInfo[] array9 = new CSharpArgumentInfo[_0019._0017(1416)];
							array9[_0019._0017(1420)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1424), null);
							_003C_003Eo__68._003C_003Ep__6 = CallSite<Func<CallSite, object, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.GetMember((CSharpBinderFlags)flags9, name6, typeFromHandle9, array9));
						}
						if (target5(_003C_003Ep__5, target6(_003C_003Ep__6, _003C_003Eo__68._003C_003Ep__6.Target(_003C_003Eo__68._003C_003Ep__6, ((Selector)cmb_script).SelectedItem), _0011._0017(2308))))
						{
							((UIElement)cmb_keyboard).IsEnabled = (byte)_0019._0017(1428) != 0;
							((UIElement)btnTutor).IsEnabled = (byte)_0019._0017(1432) != 0;
							Settings.Default.DefaultFontFamily = Settings.Default.DefaultSymFont;
						}
						else
						{
							if (_003C_003Eo__68._003C_003Ep__11 == null)
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
								int flags10 = _0019._0017(1436);
								int operation4 = _0019._0017(1440);
								Type? typeFromHandle10 = typeof(MainWindow);
								CSharpArgumentInfo[] array10 = new CSharpArgumentInfo[_0019._0017(1444)];
								array10[_0019._0017(1448)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1452), null);
								_003C_003Eo__68._003C_003Ep__11 = CallSite<Func<CallSite, object, bool>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.UnaryOperation((CSharpBinderFlags)flags10, (ExpressionType)operation4, typeFromHandle10, array10));
							}
							Func<CallSite, object, bool> target7 = _003C_003Eo__68._003C_003Ep__11.Target;
							CallSite<Func<CallSite, object, bool>> _003C_003Ep__7 = _003C_003Eo__68._003C_003Ep__11;
							if (_003C_003Eo__68._003C_003Ep__10 == null)
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
								int flags11 = _0019._0017(1456);
								string name7 = _0011._0017(2809);
								Type? typeFromHandle11 = typeof(MainWindow);
								CSharpArgumentInfo[] array11 = new CSharpArgumentInfo[_0019._0017(1460)];
								array11[_0019._0017(1464)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1468), null);
								array11[_0019._0017(1472)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1476), null);
								_003C_003Eo__68._003C_003Ep__10 = CallSite<Func<CallSite, object, string, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.InvokeMember((CSharpBinderFlags)flags11, name7, null, typeFromHandle11, array11));
							}
							Func<CallSite, object, string, object> target8 = _003C_003Eo__68._003C_003Ep__10.Target;
							CallSite<Func<CallSite, object, string, object>> _003C_003Ep__8 = _003C_003Eo__68._003C_003Ep__10;
							if (_003C_003Eo__68._003C_003Ep__9 == null)
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
								int flags12 = _0019._0017(1480);
								string name8 = _0011._0017(2225);
								Type? typeFromHandle12 = typeof(MainWindow);
								CSharpArgumentInfo[] array12 = new CSharpArgumentInfo[_0019._0017(1484)];
								array12[_0019._0017(1488)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1492), null);
								_003C_003Eo__68._003C_003Ep__9 = CallSite<Func<CallSite, object, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.GetMember((CSharpBinderFlags)flags12, name8, typeFromHandle12, array12));
							}
							if (target7(_003C_003Ep__7, target8(_003C_003Ep__8, _003C_003Eo__68._003C_003Ep__9.Target(_003C_003Eo__68._003C_003Ep__9, ((Selector)cmb_script).SelectedItem), _0011._0017(2222))))
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
								Settings.Default.DefaultFontFamily = Settings.Default.DefaultEngFont;
							}
						}
					}
				}
				Settings @default = Settings.Default;
				if (_003C_003Eo__68._003C_003Ep__13 == null)
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
					_003C_003Eo__68._003C_003Ep__13 = CallSite<Func<CallSite, object, string>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.Convert((CSharpBinderFlags)_0019._0017(1496), typeof(string), typeof(MainWindow)));
				}
				Func<CallSite, object, string> target9 = _003C_003Eo__68._003C_003Ep__13.Target;
				CallSite<Func<CallSite, object, string>> _003C_003Ep__9 = _003C_003Eo__68._003C_003Ep__13;
				if (_003C_003Eo__68._003C_003Ep__12 == null)
				{
					int flags13 = _0019._0017(1500);
					string name9 = _0011._0017(2225);
					Type? typeFromHandle13 = typeof(MainWindow);
					CSharpArgumentInfo[] array13 = new CSharpArgumentInfo[_0019._0017(1504)];
					array13[_0019._0017(1508)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1512), null);
					_003C_003Eo__68._003C_003Ep__12 = CallSite<Func<CallSite, object, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.GetMember((CSharpBinderFlags)flags13, name9, typeFromHandle13, array13));
				}
				@default.DefaultScript = target9(_003C_003Ep__9, _003C_003Eo__68._003C_003Ep__12.Target(_003C_003Eo__68._003C_003Ep__12, ((Selector)cmb_script).SelectedItem));
				((SettingsBase)Settings.Default).Save();
				if (Compose != null)
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
					if (Compose.ChangeScript(Convert.ToInt32(Settings.Default.DefaultScript)) != 0L)
					{
						while (true)
						{
							switch (1)
							{
							case 0:
								break;
							default:
								throw new Exception(_0011._0017(2822));
							}
						}
					}
				}
				if (lst_Recent != null)
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
					((Control)lst_Recent).FontFamily = new FontFamily(Settings.Default.DefaultFontFamily);
				}
				if (_003C_003Eo__68._003C_003Ep__17 == null)
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
					int flags14 = _0019._0017(1516);
					int operation5 = _0019._0017(1520);
					Type? typeFromHandle14 = typeof(MainWindow);
					CSharpArgumentInfo[] array14 = new CSharpArgumentInfo[_0019._0017(1524)];
					array14[_0019._0017(1528)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1532), null);
					_003C_003Eo__68._003C_003Ep__17 = CallSite<Func<CallSite, object, bool>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.UnaryOperation((CSharpBinderFlags)flags14, (ExpressionType)operation5, typeFromHandle14, array14));
				}
				Func<CallSite, object, bool> target10 = _003C_003Eo__68._003C_003Ep__17.Target;
				CallSite<Func<CallSite, object, bool>> _003C_003Ep__10 = _003C_003Eo__68._003C_003Ep__17;
				if (_003C_003Eo__68._003C_003Ep__16 == null)
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
					int flags15 = _0019._0017(1536);
					int operation6 = _0019._0017(1540);
					Type? typeFromHandle15 = typeof(MainWindow);
					CSharpArgumentInfo[] array15 = new CSharpArgumentInfo[_0019._0017(1544)];
					array15[_0019._0017(1548)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1552), null);
					_003C_003Eo__68._003C_003Ep__16 = CallSite<Func<CallSite, object, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.UnaryOperation((CSharpBinderFlags)flags15, (ExpressionType)operation6, typeFromHandle15, array15));
				}
				Func<CallSite, object, object> target11 = _003C_003Eo__68._003C_003Ep__16.Target;
				CallSite<Func<CallSite, object, object>> _003C_003Ep__11 = _003C_003Eo__68._003C_003Ep__16;
				if (_003C_003Eo__68._003C_003Ep__15 == null)
				{
					int flags16 = _0019._0017(1556);
					string name10 = _0011._0017(2809);
					Type? typeFromHandle16 = typeof(MainWindow);
					CSharpArgumentInfo[] array16 = new CSharpArgumentInfo[_0019._0017(1560)];
					array16[_0019._0017(1564)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1568), null);
					array16[_0019._0017(1572)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1576), null);
					_003C_003Eo__68._003C_003Ep__15 = CallSite<Func<CallSite, object, string, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.InvokeMember((CSharpBinderFlags)flags16, name10, null, typeFromHandle16, array16));
				}
				Func<CallSite, object, string, object> target12 = _003C_003Eo__68._003C_003Ep__15.Target;
				CallSite<Func<CallSite, object, string, object>> _003C_003Ep__12 = _003C_003Eo__68._003C_003Ep__15;
				if (_003C_003Eo__68._003C_003Ep__14 == null)
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
					int flags17 = _0019._0017(1580);
					string name11 = _0011._0017(2225);
					Type? typeFromHandle17 = typeof(MainWindow);
					CSharpArgumentInfo[] array17 = new CSharpArgumentInfo[_0019._0017(1584)];
					array17[_0019._0017(1588)] = CSharpArgumentInfo.Create((CSharpArgumentInfoFlags)_0019._0017(1592), null);
					_003C_003Eo__68._003C_003Ep__14 = CallSite<Func<CallSite, object, object>>.Create(Microsoft.CSharp.RuntimeBinder.Binder.GetMember((CSharpBinderFlags)flags17, name11, typeFromHandle17, array17));
				}
				if (!target10(_003C_003Ep__10, target11(_003C_003Ep__11, target12(_003C_003Ep__12, _003C_003Eo__68._003C_003Ep__14.Target(_003C_003Eo__68._003C_003Ep__14, ((Selector)cmb_script).SelectedItem), _0011._0017(2308)))))
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
					if (DrawSettings != null)
					{
						FillFontDetails();
						FillKeyboardDetails();
					}
					FontHandler = new FontHandler(Settings.Default.DefaultScript);
					ChangeKeyboardTutorLayout();
					return;
				}
			}
		}
		catch (SLCOperationException ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void cmb_Font_SelectionChanged(object sender, SelectionChangedEventArgs e)
	{
		//IL_0158: Unknown result type (might be due to invalid IL or missing references)
		//IL_015d: Unknown result type (might be due to invalid IL or missing references)
		//IL_016b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0170: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (cmb_Font == null)
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
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				if (((Selector)cmb_Font).SelectedIndex == _0019._0017(1596))
				{
					return;
				}
				while (true)
				{
					switch (1)
					{
					case 0:
						continue;
					}
					DoAction();
					AdornerActions.SLXFont = DrawFont[((Selector)cmb_script).SelectedIndex][((Selector)cmb_Font).SelectedIndex];
					if (MainCanvas.ElementSelected == null)
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
						CanvasControl canvasControl = MainCanvas.ElementSelected as CanvasControl;
						canvasControl.SLXFont = DrawFont[((Selector)cmb_script).SelectedIndex][((Selector)cmb_Font).SelectedIndex];
						Adorner[] adorners = AdornerLayer.GetAdornerLayer((Visual)(object)canvasControl).GetAdorners((UIElement)(object)canvasControl);
						if (adorners == null)
						{
							return;
						}
						while (true)
						{
							switch (7)
							{
							case 0:
								continue;
							}
							if (adorners.Length <= _0019._0017(1600))
							{
								return;
							}
							while (true)
							{
								switch (4)
								{
								case 0:
									continue;
								}
								if (!(adorners[_0019._0017(1604)] is CanvasAdornerActions canvasAdornerActions))
								{
									return;
								}
								while (true)
								{
									switch (4)
									{
									case 0:
										continue;
									}
									string compliantString = FontHandler.GetCompliantString(canvasControl.SLXFont, canvasControl.InputString);
									canvasAdornerActions.ReplaceInputString(compliantString);
									return;
								}
							}
						}
					}
				}
			}
		}
		catch (SLCOperationException ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void cmb_keyboard_SelectionChanged(object sender, SelectionChangedEventArgs e)
	{
		//IL_00f9: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fe: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (Compose != null)
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
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				if (cmb_keyboard != null)
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
					if (((CollectionView)((ItemsControl)cmb_keyboard).Items).Count > _0019._0017(1608))
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
						if (((Selector)cmb_keyboard).SelectedIndex > _0019._0017(1612))
						{
							Compose.SetKeyboardLayout(Convert.ToInt32(((Selector)cmb_script).SelectedValue), ((Selector)cmb_keyboard).SelectedItem.ToString().ToUpper());
							Settings.Default.KeyboardLayoutIndex[((Selector)cmb_script).SelectedIndex] = ((Selector)cmb_keyboard).SelectedIndex.ToString();
							((SettingsBase)Settings.Default).Save();
						}
					}
				}
			}
			ChangeKeyboardTutorLayout();
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void Window_Closed(object sender, EventArgs e)
	{
		//IL_005b: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			SaveSettings();
			if (Compose != null)
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
				Compose.CloseShreeSetup();
				Compose.Unload();
			}
			if (GObjects.LM == null)
			{
				return;
			}
			while (true)
			{
				switch (7)
				{
				case 0:
					continue;
				}
				GObjects.LM.SLM2();
				return;
			}
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void HandleKeyDownEvent(object sender, KeyEventArgs e)
	{
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_000f: Unknown result type (might be due to invalid IL or missing references)
		//IL_001a: Invalid comparison between Unknown and I4
		//IL_05cc: Unknown result type (might be due to invalid IL or missing references)
		//IL_05d1: Unknown result type (might be due to invalid IL or missing references)
		//IL_02f5: Unknown result type (might be due to invalid IL or missing references)
		//IL_02fa: Unknown result type (might be due to invalid IL or missing references)
		//IL_0306: Unknown result type (might be due to invalid IL or missing references)
		//IL_0311: Invalid comparison between Unknown and I4
		//IL_0587: Unknown result type (might be due to invalid IL or missing references)
		//IL_0596: Unknown result type (might be due to invalid IL or missing references)
		//IL_05a1: Invalid comparison between Unknown and I4
		//IL_0317: Unknown result type (might be due to invalid IL or missing references)
		//IL_031c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0328: Invalid comparison between Unknown and I4
		//IL_05a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_05a8: Unknown result type (might be due to invalid IL or missing references)
		//IL_05b4: Unknown result type (might be due to invalid IL or missing references)
		//IL_0386: Unknown result type (might be due to invalid IL or missing references)
		//IL_038b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0397: Invalid comparison between Unknown and I4
		//IL_0033: Unknown result type (might be due to invalid IL or missing references)
		//IL_0038: Unknown result type (might be due to invalid IL or missing references)
		//IL_0044: Invalid comparison between Unknown and I4
		//IL_03ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_03b2: Unknown result type (might be due to invalid IL or missing references)
		//IL_03be: Invalid comparison between Unknown and I4
		//IL_004d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0052: Unknown result type (might be due to invalid IL or missing references)
		//IL_005e: Invalid comparison between Unknown and I4
		//IL_03c7: Unknown result type (might be due to invalid IL or missing references)
		//IL_03cc: Unknown result type (might be due to invalid IL or missing references)
		//IL_03d8: Invalid comparison between Unknown and I4
		//IL_0071: Unknown result type (might be due to invalid IL or missing references)
		//IL_0076: Unknown result type (might be due to invalid IL or missing references)
		//IL_0082: Invalid comparison between Unknown and I4
		//IL_03eb: Unknown result type (might be due to invalid IL or missing references)
		//IL_03fa: Invalid comparison between Unknown and I4
		//IL_009f: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a4: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b0: Invalid comparison between Unknown and I4
		//IL_040d: Unknown result type (might be due to invalid IL or missing references)
		//IL_041c: Invalid comparison between Unknown and I4
		//IL_00c3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d4: Invalid comparison between Unknown and I4
		//IL_0439: Unknown result type (might be due to invalid IL or missing references)
		//IL_0448: Invalid comparison between Unknown and I4
		//IL_01c9: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ce: Unknown result type (might be due to invalid IL or missing references)
		//IL_01da: Invalid comparison between Unknown and I4
		//IL_0471: Unknown result type (might be due to invalid IL or missing references)
		//IL_0476: Unknown result type (might be due to invalid IL or missing references)
		//IL_0482: Invalid comparison between Unknown and I4
		//IL_020c: Unknown result type (might be due to invalid IL or missing references)
		//IL_021b: Invalid comparison between Unknown and I4
		//IL_04a9: Unknown result type (might be due to invalid IL or missing references)
		//IL_04ae: Unknown result type (might be due to invalid IL or missing references)
		//IL_04ba: Invalid comparison between Unknown and I4
		//IL_024d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0252: Unknown result type (might be due to invalid IL or missing references)
		//IL_025e: Invalid comparison between Unknown and I4
		//IL_04eb: Unknown result type (might be due to invalid IL or missing references)
		//IL_04fa: Invalid comparison between Unknown and I4
		//IL_029c: Unknown result type (might be due to invalid IL or missing references)
		//IL_02a1: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ad: Invalid comparison between Unknown and I4
		//IL_0521: Unknown result type (might be due to invalid IL or missing references)
		//IL_0526: Unknown result type (might be due to invalid IL or missing references)
		//IL_0532: Invalid comparison between Unknown and I4
		try
		{
			if ((Keyboard.Modifiers & _0019._0017(1616)) == _0019._0017(1620))
			{
				while (true)
				{
					switch (2)
					{
					case 0:
						break;
					default:
						if (1 == 0)
						{
							/*OpCode not supported: LdMemberToken*/;
						}
						if ((int)e.Key == _0019._0017(1624))
						{
							RedoAction();
						}
						if ((int)e.Key == _0019._0017(1628))
						{
							ModifyFontSelection(_0019._0017(1632));
						}
						if ((int)e.Key == _0019._0017(1636))
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
							ModifyFontSelection(_0019._0017(1640));
						}
						if ((int)e.Key == _0019._0017(1644))
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
							SaveAs();
						}
						if ((int)e.Key == _0019._0017(1648))
						{
							TabControl tabPreviewRecent = TabPreviewRecent;
							int selectedIndex;
							if (((Selector)TabPreviewRecent).SelectedIndex != 0)
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
								selectedIndex = _0019._0017(1652);
							}
							else
							{
								selectedIndex = _0019._0017(1656);
							}
							((Selector)tabPreviewRecent).SelectedIndex = selectedIndex;
							if (((Selector)TabPreviewRecent).SelectedIndex == 0)
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
								((Selector)lst_Preview).SelectedIndex = ((((Selector)lst_Preview).SelectedIndex == _0019._0017(1660)) ? _0019._0017(1664) : ((Selector)lst_Preview).SelectedIndex);
								((UIElement)lst_Preview).Focus();
							}
							else
							{
								ListBox obj = lst_Recent;
								int selectedIndex2;
								if (((Selector)lst_Recent).SelectedIndex != _0019._0017(1668))
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
									selectedIndex2 = ((Selector)lst_Recent).SelectedIndex;
								}
								else
								{
									selectedIndex2 = _0019._0017(1672);
								}
								((Selector)obj).SelectedIndex = selectedIndex2;
								((UIElement)lst_Recent).Focus();
							}
						}
						if ((int)e.Key == _0019._0017(1676))
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
							MainCanvasAdornerActions canvasAdornerActionsObject = MainCanvas.GetCanvasAdornerActionsObject();
							if (canvasAdornerActionsObject != null)
							{
								_ = MainCanvas.ElementSelected;
								canvasAdornerActionsObject.AddCanvasObject_MouseUp(null, null);
							}
						}
						if ((int)e.Key == _0019._0017(1680))
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
							MainCanvasAdornerActions canvasAdornerActionsObject2 = MainCanvas.GetCanvasAdornerActionsObject();
							if (canvasAdornerActionsObject2 != null)
							{
								_ = MainCanvas.ElementSelected;
								canvasAdornerActionsObject2.RandomizeStrings_MouseUp(null, null);
							}
						}
						if ((int)e.Key == _0019._0017(1684))
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
							MainCanvasAdornerActions canvasAdornerActionsObject3 = MainCanvas.GetCanvasAdornerActionsObject();
							if (canvasAdornerActionsObject3 != null)
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
								_ = MainCanvas.ElementSelected;
								canvasAdornerActionsObject3.RandomizeFonts_MouseUp(null, null);
							}
						}
						if ((int)e.Key == _0019._0017(1688))
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
							MainCanvasAdornerActions canvasAdornerActionsObject4 = MainCanvas.GetCanvasAdornerActionsObject();
							if (canvasAdornerActionsObject4 != null)
							{
								_ = MainCanvas.ElementSelected;
								canvasAdornerActionsObject4.RemoveAll_MouseUp(null, null);
							}
						}
						((RoutedEventArgs)e).Handled = (byte)_0019._0017(1692) != 0;
						return;
					}
				}
			}
			if ((Keyboard.Modifiers & _0019._0017(1696)) == _0019._0017(1700))
			{
				if ((int)e.Key == _0019._0017(1704))
				{
					((Panel)MainCanvas).Children.Clear();
					MainCanvasAdornerActions canvasAdornerActionsObject5 = MainCanvas.GetCanvasAdornerActionsObject();
					if (canvasAdornerActionsObject5 != null)
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
						_ = MainCanvas.ElementSelected;
						canvasAdornerActionsObject5.AddCanvasObject_MouseUp(null, null);
					}
					UpdatePreviewList((byte)_0019._0017(1708) != 0, null);
					EnableDisableSaveButtons();
				}
				if ((int)e.Key == _0019._0017(1712))
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
					OpenFile();
				}
				if ((int)e.Key == _0019._0017(1716))
				{
					SaveRecentText();
				}
				if ((int)e.Key == _0019._0017(1720))
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
					UndoAction();
				}
				if ((int)e.Key == _0019._0017(1724))
				{
					ModifyPreviewSelection(_0019._0017(1728));
				}
				if ((int)e.Key == _0019._0017(1732))
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
					ModifyPreviewSelection(_0019._0017(1736));
				}
				if ((int)e.Key == _0019._0017(1740) && MainCanvas.ElementSelected != null)
				{
					(MainCanvas.ElementSelected as CanvasControl).HighlightNextCharacter();
				}
				if ((int)e.Key == _0019._0017(1744) && MainCanvas.ElementSelected != null)
				{
					(MainCanvas.ElementSelected as CanvasControl).HighlightPreviousCharacter();
				}
				if ((int)e.Key == _0019._0017(1748) && MainCanvas.ElementSelected != null)
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
					(MainCanvas.ElementSelected as CanvasControl).EditString();
				}
				if ((int)e.Key == _0019._0017(1752) && MainCanvas.ElementSelected != null)
				{
					(MainCanvas.ElementSelected as CanvasControl).RemoveFromCanvas();
				}
				if ((int)e.Key == _0019._0017(1756))
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
					if (MainCanvas.ElementSelected != null)
					{
						UpdatePreviewList((byte)_0019._0017(1760) != 0, null);
						(MainCanvas.ElementSelected as CanvasControl).RandomizeInputString();
					}
				}
				((RoutedEventArgs)e).Handled = (byte)_0019._0017(1764) != 0;
			}
			else if ((Keyboard.Modifiers & _0019._0017(1768)) != _0019._0017(1772))
			{
				_ = Keyboard.Modifiers & _0019._0017(1776);
				_0019._0017(1780);
			}
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void lst_Recent_MouseDoubleClick(object sender, MouseButtonEventArgs e)
	{
		//IL_0027: Unknown result type (might be due to invalid IL or missing references)
		//IL_002c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0038: Unknown result type (might be due to invalid IL or missing references)
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			ReplaceCanvasObjectsFromRecent(sender);
		}
		catch (SLCCompositionException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
			GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionReplaceFromRecent, Calligrapher.Properties.Resources.MsgReplaceFromRecent);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void lst_Recent_KeyUp(object sender, KeyEventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_0010: Invalid comparison between Unknown and I4
		//IL_004a: Unknown result type (might be due to invalid IL or missing references)
		//IL_004f: Unknown result type (might be due to invalid IL or missing references)
		//IL_005b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0060: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if ((int)e.Key != _0019._0017(1784))
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
				ReplaceCanvasObjectsFromRecent(sender);
				return;
			}
		}
		catch (SLCCompositionException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
			GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionReplaceFromRecent, Calligrapher.Properties.Resources.MsgReplaceFromRecent);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void btnClearAllQuicksave_Click(object sender, RoutedEventArgs e)
	{
		((ItemsControl)lst_Recent).ItemsSource = null;
		RecentCollection.Clear();
		((ContentControl)t2ToolTip).Content = _0019._0017(1788);
	}

	private void btnRemoveQuickSave_Click(object sender, RoutedEventArgs e)
	{
		if (((Selector)lst_Recent).SelectedIndex <= _0019._0017(1792))
		{
			return;
		}
		while (true)
		{
			switch (5)
			{
			case 0:
				continue;
			}
			if (1 == 0)
			{
				/*OpCode not supported: LdMemberToken*/;
			}
			RecentCollection.RemoveAt(((Selector)lst_Recent).SelectedIndex);
			((CollectionView)((ItemsControl)lst_Recent).Items).Refresh();
			((Selector)lst_Recent).SelectedIndex = _0019._0017(1796);
			return;
		}
	}

	private void lst_Preview_KeyUp(object sender, KeyEventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_0006: Unknown result type (might be due to invalid IL or missing references)
		//IL_0012: Invalid comparison between Unknown and I4
		//IL_0037: Unknown result type (might be due to invalid IL or missing references)
		//IL_003c: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if ((int)e.Key != _0019._0017(1800))
			{
				return;
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
				ReplaceWordFromList(sender);
				return;
			}
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void MainCanvas_SizeChanged(object sender, SizeChangedEventArgs e)
	{
	}

	private void MainCanvas_PreviewMouseLeftButtonUp(object sender, MouseButtonEventArgs e)
	{
		//IL_0299: Unknown result type (might be due to invalid IL or missing references)
		//IL_029e: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			Mouse.OverrideCursor = Cursors.Wait;
			CanvasControl canvasControl;
			if (sender.GetType() == typeof(DragCanvas))
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
				DoAction();
				DragCanvas dragCanvas = (DragCanvas)sender;
				if (dragCanvas.ElementSelected != null)
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
					canvasControl = dragCanvas.ElementSelected as CanvasControl;
					if (canvasControl.SLXFont.GetFontName().ToUpper().Contains(_0011._0017(2371)))
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
						if (!((Selector)cmb_script).SelectedValue.Equals(_0011._0017(2302)))
						{
							goto IL_011b;
						}
					}
					if (canvasControl.SLXFont.GetFontName().ToUpper().Contains(_0011._0017(2399)) && !((Selector)cmb_script).SelectedValue.Equals(_0011._0017(2305)))
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
						goto IL_011b;
					}
					goto IL_01b5;
				}
				MainCanvas.RemoveSelection();
				UpdatePreviewList((byte)_0019._0017(1812) != 0, null);
			}
			goto IL_028a;
			IL_028a:
			Mouse.OverrideCursor = null;
			return;
			IL_011b:
			if (canvasControl.SLXFont.GetFontName().ToUpper().Contains(_0011._0017(2371)))
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
				((Selector)cmb_script).SelectedValue = _0011._0017(2302);
			}
			else if (canvasControl.SLXFont.GetFontName().ToUpper().Contains(_0011._0017(2399)))
			{
				((Selector)cmb_script).SelectedValue = _0011._0017(2305);
			}
			MainCanvas.AddSelection(canvasControl);
			goto IL_01b5;
			IL_01b5:
			int num = _0019._0017(1804);
			while (true)
			{
				if (num < DrawFont[((Selector)cmb_script).SelectedIndex].Count)
				{
					if (DrawFont[((Selector)cmb_script).SelectedIndex][num] != null)
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
						if (DrawFont[((Selector)cmb_script).SelectedIndex][num].GetFontName().Equals(canvasControl.SLXFont.GetFontName()))
						{
							((Selector)cmb_Font).SelectedIndex = num;
							break;
						}
					}
					num += _0019._0017(1808);
					continue;
				}
				while (true)
				{
					switch (6)
					{
					case 0:
						continue;
					}
					break;
				}
				break;
			}
			goto IL_028a;
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void MainCanvas_PreviewMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
	{
		//IL_0062: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (!(sender.GetType() == typeof(DragCanvas)) || ((DragCanvas)sender).ElementSelected != null)
			{
				return;
			}
			while (true)
			{
				switch (7)
				{
				case 0:
					continue;
				}
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				MainCanvas.RemoveSelection();
				UpdatePreviewList((byte)_0019._0017(1816) != 0, null);
				return;
			}
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	public void UpdatePreviewList(bool show, RTBEx rtbex)
	{
		//IL_0006: Unknown result type (might be due to invalid IL or missing references)
		if ((int)((UIElement)lst_Preview).Visibility != 0)
		{
			return;
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
			((ItemsControl)lst_Preview).ItemsSource = null;
			if (show)
			{
				while (true)
				{
					switch (1)
					{
					case 0:
						break;
					default:
					{
						Mouse.OverrideCursor = Cursors.Wait;
						DrawCharList = null;
						string text = rtbex.GetCaretChar().ToString() ?? "";
						if (!(text == _0011._0017(2887)))
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
							if (!(text == _0011._0017(94)))
							{
								if (!FontHandler.GetCharList(DrawFont[((Selector)cmb_script).SelectedIndex][((Selector)cmb_Font).SelectedIndex], text, out DrawCharList))
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
									if (DrawCharList.Count == 0)
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
										DrawCharList.Add(text);
									}
								}
								rtbex.GetPreviewList(ref DrawCharList);
								DrawImageList.Clear();
								new List<Canvas>();
								_ = DrawFont[((Selector)cmb_script).SelectedIndex][((Selector)cmb_Font).SelectedIndex];
								((DispatcherObject)this).Dispatcher.BeginInvoke((Delegate)(Action)delegate
								{
									//IL_0076: Unknown result type (might be due to invalid IL or missing references)
									using (List<string>.Enumerator enumerator = DrawCharList.GetEnumerator())
									{
										while (enumerator.MoveNext())
										{
											string current = enumerator.Current;
											List<CanvasObject> list = new List<CanvasObject>();
											CanvasObject @object = CanvasObject.GetObject(current, DrawFont[((Selector)cmb_script).SelectedIndex][((Selector)cmb_Font).SelectedIndex], new Rect(_0019._0017(2252), _0019._0017(2260), _0019._0017(2268), _0019._0017(2276)), DrawSettings);
											list.Add(@object);
											IFileExport instance = FileExportFactory.GetInstance((FileTypes)_0019._0017(2284), "", list, (byte)_0019._0017(2288) != 0);
											if (instance != null)
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
												instance.SetDimension(_0019._0017(2292), _0019._0017(2296));
												instance.SetBackground((BackGround)_0019._0017(2300), _0011._0017(278));
												instance.SetDpi(_0019._0017(2304), _0019._0017(2312));
												instance.SetFontColorSpace((ColorSpace)_0019._0017(2320), _0011._0017(278));
												Bitmap val = instance.ExportImage();
												DrawImageList.Add(BitmapConversion.ToBitmapImage(val));
											}
										}
										while (true)
										{
											switch (3)
											{
											case 0:
												break;
											default:
												goto end_IL_0167;
											}
											continue;
											end_IL_0167:
											break;
										}
									}
									((ItemsControl)lst_Preview).ItemsSource = DrawImageList;
									Mouse.OverrideCursor = null;
								}, new object[_0019._0017(1820)]);
								return;
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
						Mouse.OverrideCursor = null;
						return;
					}
					}
				}
			}
			((ItemsControl)lst_Preview).ItemsSource = null;
			return;
		}
	}

	private void ReplaceWordFromList(object sender)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_0007: Expected O, but got Unknown
		ListBox val = (ListBox)sender;
		if (val.SelectedItems.Count != _0019._0017(1824))
		{
			return;
		}
		while (true)
		{
			switch (4)
			{
			case 0:
				continue;
			}
			if (1 == 0)
			{
				/*OpCode not supported: LdMemberToken*/;
			}
			DoAction();
			CanvasControl canvasControl = MainCanvas.ElementSelected as CanvasControl;
			Adorner[] adorners = AdornerLayer.GetAdornerLayer((Visual)(object)canvasControl).GetAdorners((UIElement)(object)canvasControl);
			if (adorners != null)
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
				if (adorners.Length > _0019._0017(1828) && adorners[_0019._0017(1832)] is CanvasAdornerActions canvasAdornerActions)
				{
					string replacement = DrawCharList[((Selector)val).SelectedIndex];
					canvasAdornerActions.ReplaceWordUnderCaret(replacement);
				}
			}
			if (DrawImageList.Count <= _0019._0017(1836))
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
				((ItemsControl)lst_Preview).ItemsSource = DrawImageList;
				return;
			}
		}
	}

	private void ModifyPreviewSelection(int delta)
	{
		if (((CollectionView)((ItemsControl)lst_Preview).Items).Count == 0)
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
					return;
				}
			}
		}
		if (delta > _0019._0017(1840) && ((Selector)lst_Preview).SelectedIndex <= _0019._0017(1844))
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
			((Selector)lst_Preview).SelectedIndex = _0019._0017(1848);
		}
		else if (delta < _0019._0017(1852) && ((Selector)lst_Preview).SelectedIndex == ((CollectionView)((ItemsControl)lst_Preview).Items).Count - _0019._0017(1856))
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
			((Selector)lst_Preview).SelectedIndex = ((CollectionView)((ItemsControl)lst_Preview).Items).Count - _0019._0017(1860);
		}
		else if (delta > _0019._0017(1864))
		{
			ListBox obj = lst_Preview;
			int selectedIndex = ((Selector)obj).SelectedIndex;
			((Selector)obj).SelectedIndex = selectedIndex - _0019._0017(1868);
		}
		else
		{
			ListBox obj2 = lst_Preview;
			int selectedIndex = ((Selector)obj2).SelectedIndex;
			((Selector)obj2).SelectedIndex = selectedIndex + _0019._0017(1872);
		}
		lst_Preview.ScrollIntoView(((Selector)lst_Preview).SelectedItem);
	}

	private void ModifyFontSelection(int delta)
	{
		if (((CollectionView)((ItemsControl)cmb_Font).Items).Count == 0)
		{
			return;
		}
		if (delta > _0019._0017(1876) && ((Selector)cmb_Font).SelectedIndex == 0)
		{
			((Selector)cmb_Font).SelectedIndex = _0019._0017(1880);
			return;
		}
		if (delta < _0019._0017(1884))
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
			if (((Selector)cmb_Font).SelectedIndex == ((CollectionView)((ItemsControl)cmb_Font).Items).Count - _0019._0017(1888))
			{
				((Selector)cmb_Font).SelectedIndex = ((CollectionView)((ItemsControl)cmb_Font).Items).Count - _0019._0017(1892);
				return;
			}
		}
		if (delta > _0019._0017(1896))
		{
			ComboBox obj = cmb_Font;
			int selectedIndex = ((Selector)obj).SelectedIndex;
			((Selector)obj).SelectedIndex = selectedIndex - _0019._0017(1900);
		}
		else
		{
			ComboBox obj2 = cmb_Font;
			int selectedIndex = ((Selector)obj2).SelectedIndex;
			((Selector)obj2).SelectedIndex = selectedIndex + _0019._0017(1904);
		}
	}

	private void ReplaceCanvasObjectsFromRecent(object sender)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_0007: Expected O, but got Unknown
		try
		{
			ListBox val = (ListBox)sender;
			if (val.SelectedItems.Count != _0019._0017(1908))
			{
				return;
			}
			while (true)
			{
				switch (7)
				{
				case 0:
					continue;
				}
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				RTFToolTip rTFToolTip = RecentCollection[((Selector)val).SelectedIndex];
				MainCanvas.LoadCanvasObjects(DrawSettings, rTFToolTip.CanvasObjects);
				EnableDisableSaveButtons();
				UpdatePreviewList((byte)_0019._0017(1912) != 0, null);
				return;
			}
		}
		catch (ArgumentException ex)
		{
			throw new SLCCompositionException(ex);
		}
	}

	private void SaveRecentText()
	{
		//IL_0177: Unknown result type (might be due to invalid IL or missing references)
		//IL_017c: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (((Panel)MainCanvas).Children.Count <= _0019._0017(1916))
			{
				return;
			}
			while (true)
			{
				switch (7)
				{
				case 0:
					continue;
				}
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				List<CanvasObject> canvasObjects = MainCanvas.GetCanvasObjects();
				if (canvasObjects.Count <= _0019._0017(1920))
				{
					return;
				}
				while (true)
				{
					switch (7)
					{
					case 0:
						continue;
					}
					RTFToolTip rTFToolTip = new RTFToolTip(canvasObjects, IsDemo);
					if (RecentCollection.Count == _0019._0017(1924))
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
						RecentCollection.RemoveAt(RecentCollection.Count - _0019._0017(1928));
					}
					if (rTFToolTip != null)
					{
						RecentCollection.Insert(_0019._0017(1932), rTFToolTip);
					}
					else
					{
						GObjects.Log.GTLogDebugMsg(_0011._0017(2890));
					}
					((ItemsControl)lst_Recent).ItemsSource = null;
					((ItemsControl)lst_Recent).ItemsSource = RecentCollection;
					((ContentControl)t2ToolTip).Content = ((CollectionView)((ItemsControl)lst_Recent).Items).Count;
					t2ToolTip.PlacementTarget = (UIElement)(object)t2;
					t2ToolTip.IsOpen = (byte)_0019._0017(1936) != 0;
					PopupTimer.Start();
					return;
				}
			}
		}
		catch (ArgumentException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
			GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionSaveRecent, Calligrapher.Properties.Resources.MsgSaveRecent);
		}
	}

	private void SaveAs()
	{
		//IL_0118: Unknown result type (might be due to invalid IL or missing references)
		//IL_011d: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e6: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (((Panel)MainCanvas).Children.Count <= _0019._0017(1940))
			{
				return;
			}
			while (true)
			{
				switch (4)
				{
				case 0:
					continue;
				}
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				if (!((UIElement)btnExport).IsEnabled)
				{
					while (true)
					{
						switch (7)
						{
						case 0:
							break;
						default:
							return;
						}
					}
				}
				if (DrawFont[((Selector)cmb_script).SelectedIndex][((Selector)cmb_Font).SelectedIndex] != null)
				{
					if (Compose != null)
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
						Compose.CloseShreeSetup();
					}
					ExportWindow exportWindow = new ExportWindow(MainCanvas.GetCanvasObjects(), DrawSettings);
					if (exportWindow != null)
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
						((Window)exportWindow).Owner = (Window)(object)this;
						((Window)exportWindow).ShowDialog();
					}
					else
					{
						GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionExport, Calligrapher.Properties.Resources.MsgExportFailed);
						GObjects.Log.GTLogDebugMsg(_0011._0017(2937));
					}
				}
				else
				{
					GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionExport, Calligrapher.Properties.Resources.MsgExportFailed);
				}
				if (Compose != null && Compose.Setup() != 0L)
				{
					throw new Exception(_0011._0017(2980));
				}
				return;
			}
		}
		catch (Exception)
		{
			throw;
		}
	}

	private void LoadRecentStringsFromFile()
	{
		try
		{
			if (File.Exists(CLFileName))
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
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				LoadFile(CLFileName);
			}
			else if (File.Exists(AppPathManager.GetAutosaveFile()))
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
				LoadFile(AppPathManager.GetAutosaveFile());
			}
			if (!File.Exists(AppPathManager.GetRecentsFile()))
			{
				return;
			}
			while (true)
			{
				switch (1)
				{
				case 0:
					continue;
				}
				((ItemsControl)lst_Recent).ItemsSource = null;
				((ItemsControl)lst_Recent).Items.Clear();
				RecentCollection.Clear();
				List<RTFToolTip> list = RTFToolTip.LoadFile(AppPathManager.GetRecentsFile());
				if (list != null)
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
					using List<RTFToolTip>.Enumerator enumerator = list.GetEnumerator();
					while (enumerator.MoveNext())
					{
						RTFToolTip current = enumerator.Current;
						for (int i = _0019._0017(1944); i < current.CanvasObjects.Count; i += _0019._0017(1976))
						{
							int num = DrawFont.Length;
							while ((num -= _0019._0017(1968)) < DrawFont.Length)
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
								if (num < _0019._0017(1972) || DrawFont[num][_0019._0017(1948)].GetFontName().Substring(_0019._0017(1952), _0019._0017(1956)).Equals(current.CanvasObjects[i].FontName.Substring(_0019._0017(1960), _0019._0017(1964))))
								{
									break;
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
							using List<IFontLib>.Enumerator enumerator2 = DrawFont[num].GetEnumerator();
							while (true)
							{
								if (enumerator2.MoveNext())
								{
									IFontLib current2 = enumerator2.Current;
									if (!(current2.GetFontName() == current.CanvasObjects[i].FontName))
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
										current.CanvasObjects[i].IFont = current2;
										break;
									}
									break;
								}
								while (true)
								{
									switch (5)
									{
									case 0:
										break;
									default:
										goto end_IL_0219;
									}
									continue;
									end_IL_0219:
									break;
								}
								break;
							}
						}
						RecentCollection.Add(new RTFToolTip(current.CanvasObjects, IsDemo));
					}
					while (true)
					{
						switch (2)
						{
						case 0:
							break;
						default:
							goto end_IL_027b;
						}
						continue;
						end_IL_027b:
						break;
					}
				}
				((ItemsControl)lst_Recent).ItemsSource = RecentCollection;
				((ContentControl)t2ToolTip).Content = ((CollectionView)((ItemsControl)lst_Recent).Items).Count;
				return;
			}
		}
		catch (FileNotFoundException ex)
		{
			throw new SLCIOException(ex);
		}
		catch (ArgumentException ex2)
		{
			throw new SLCCompositionException(ex2);
		}
	}

	private void SaveRecentStringsToFile()
	{
		try
		{
			List<CanvasObject> canvasObjects = MainCanvas.GetCanvasObjects();
			if (canvasObjects.Count > _0019._0017(1980))
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
				if (new SLCFileType(canvasObjects).SaveFile(AppPathManager.GetAutosaveFile()) > _0019._0017(1984))
				{
					while (true)
					{
						switch (2)
						{
						case 0:
							break;
						default:
							throw new Exception(_0011._0017(3019));
						}
					}
				}
			}
			else
			{
				try
				{
					File.Delete(AppPathManager.GetAutosaveFile());
				}
				catch (Exception)
				{
					throw;
				}
			}
			if (RecentCollection != null && RecentCollection.Count > _0019._0017(1988))
			{
				if (RTFToolTip.SaveFile(AppPathManager.GetRecentsFile(), RecentCollection) <= _0019._0017(1992))
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
					throw new Exception(_0011._0017(3050));
				}
			}
			try
			{
				File.Delete(AppPathManager.GetRecentsFile());
			}
			catch (Exception)
			{
				throw;
			}
		}
		catch (ArgumentException ex3)
		{
			throw new SLCCompositionException(ex3);
		}
	}

	private bool OpenFile()
	{
		//IL_0031: Unknown result type (might be due to invalid IL or missing references)
		//IL_0037: Expected O, but got Unknown
		bool result = (byte)_0019._0017(1996) != 0;
		try
		{
			if (Compose != null)
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
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				Compose.CloseShreeSetup();
			}
			OpenFileDialog val = new OpenFileDialog();
			((FileDialog)val).DefaultExt = _0011._0017(462);
			((FileDialog)val).Filter = _0011._0017(3095);
			if ((int?)((CommonDialog)val).ShowDialog() == _0019._0017(2000))
			{
				result = LoadFile(((FileDialog)val).FileName);
			}
		}
		catch (Exception)
		{
			result = (byte)_0019._0017(2004) != 0;
		}
		if (Compose != null && Compose.Setup() != 0L)
		{
			result = (byte)_0019._0017(2008) != 0;
			throw new Exception(_0011._0017(2980));
		}
		return result;
	}

	private bool LoadFile(string filename)
	{
		try
		{
			SLCFileType sLCFileType = SLCFileType.LoadFile(filename);
			if (sLCFileType != null)
			{
				while (true)
				{
					switch (5)
					{
					case 0:
						break;
					default:
					{
						if (1 == 0)
						{
							/*OpCode not supported: LdMemberToken*/;
						}
						for (int i = _0019._0017(2012); i < sLCFileType.CanvasObjects.Count; i += _0019._0017(2048))
						{
							int num = DrawFont.Length;
							while ((num -= _0019._0017(2036)) < DrawFont.Length)
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
								if (num < _0019._0017(2040))
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
									break;
								}
								if (DrawFont[num][_0019._0017(2016)].GetFontName().Substring(_0019._0017(2020), _0019._0017(2024)).Equals(sLCFileType.CanvasObjects[i].FontName.Substring(_0019._0017(2028), _0019._0017(2032))))
								{
									break;
								}
							}
							using (List<IFontLib>.Enumerator enumerator = DrawFont[num].GetEnumerator())
							{
								while (true)
								{
									if (!enumerator.MoveNext())
									{
										while (true)
										{
											switch (4)
											{
											case 0:
												break;
											default:
												goto end_IL_0153;
											}
											continue;
											end_IL_0153:
											break;
										}
										break;
									}
									IFontLib current = enumerator.Current;
									if (current.GetFontName() == sLCFileType.CanvasObjects[i].FontName)
									{
										sLCFileType.CanvasObjects[i].IFont = current;
										break;
									}
								}
							}
							if (sLCFileType.CanvasObjects[i].IFont == null)
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
								sLCFileType.CanvasObjects[i].IFont = DrawFont[((Selector)cmb_script).SelectedIndex][_0019._0017(2044)];
							}
						}
						while (true)
						{
							switch (6)
							{
							case 0:
								break;
							default:
								MainCanvas.LoadCanvasObjects(DrawSettings, sLCFileType.CanvasObjects);
								EnableDisableSaveButtons();
								return (byte)_0019._0017(2052) != 0;
							}
						}
					}
					}
				}
			}
		}
		catch (Exception)
		{
		}
		EnableDisableSaveButtons();
		return (byte)_0019._0017(2056) != 0;
	}

	private void EnableDisableSaveButtons()
	{
		try
		{
			if (((Panel)MainCanvas).Children.Count > _0019._0017(2060))
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
						((UIElement)btnSave).IsEnabled = (byte)_0019._0017(2064) != 0;
						((UIElement)btnExport).IsEnabled = (byte)_0019._0017(2068) != 0;
						AdornerActions.EnableActions();
						return;
					}
				}
			}
			((UIElement)btnSave).IsEnabled = (byte)_0019._0017(2072) != 0;
			((UIElement)btnExport).IsEnabled = (byte)_0019._0017(2076) != 0;
			AdornerActions.DisableActions();
		}
		catch (Exception)
		{
			throw;
		}
	}

	public void EnableDisableComboboxes(bool scripts, bool fonts, bool keyboards)
	{
		((UIElement)cmb_script).IsEnabled = scripts;
		((UIElement)cmb_Font).IsEnabled = fonts;
		((UIElement)cmb_keyboard).IsEnabled = keyboards;
	}

	public void ShowPreviewList()
	{
		if (((Selector)TabPreviewRecent).SelectedIndex == 0)
		{
			return;
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
			((Selector)TabPreviewRecent).SelectedIndex = _0019._0017(2080);
			((Selector)lst_Preview).SelectedIndex = ((((Selector)lst_Preview).SelectedIndex == _0019._0017(2084)) ? _0019._0017(2088) : ((Selector)lst_Preview).SelectedIndex);
			((UIElement)lst_Preview).Focus();
			return;
		}
	}

	private bool HandlePreviewExecutedCommand(ICommand command)
	{
		bool result = (byte)_0019._0017(2092) != 0;
		try
		{
			if (command == ApplicationCommands.Undo)
			{
				while (true)
				{
					switch (4)
					{
					case 0:
						continue;
					}
					if (1 == 0)
					{
						/*OpCode not supported: LdMemberToken*/;
					}
					UndoAction();
					result = (byte)_0019._0017(2096) != 0;
					break;
				}
			}
			else
			{
				if (command == EditingCommands.AlignJustify || command == EditingCommands.AlignLeft)
				{
					goto IL_006b;
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
				if (command == EditingCommands.AlignRight)
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
					goto IL_006b;
				}
			}
			goto end_IL_000b;
			IL_006b:
			result = (byte)_0019._0017(2100) != 0;
			end_IL_000b:;
		}
		catch (SLCCompositionException)
		{
			throw;
		}
		return result;
	}

	private void LoadSettings()
	{
		//IL_0028: Unknown result type (might be due to invalid IL or missing references)
		//IL_004e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0053: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			LoadRecentStringsFromFile();
		}
		catch (SLCIOException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
			GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionSavedStrings, Calligrapher.Properties.Resources.MsgLoadStrings);
		}
		catch (SLCCompositionException ex2)
		{
			GObjects.Log.GTLogException((Exception)ex2);
			GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionSavedStrings, Calligrapher.Properties.Resources.MsgLoadSettingsRTF);
		}
		((ApplicationSettingsBase)Settings.Default).Reload();
	}

	private void SaveSettings()
	{
		//IL_0028: Unknown result type (might be due to invalid IL or missing references)
		//IL_002d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0050: Unknown result type (might be due to invalid IL or missing references)
		//IL_0055: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			SaveRecentStringsToFile();
		}
		catch (SLCIOException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
			GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionSavedStrings, Calligrapher.Properties.Resources.MsgSavedStrings);
		}
		catch (SLCCompositionException ex2)
		{
			GObjects.Log.GTLogException((Exception)ex2);
			GObjects.Message.ShowExclamation(Calligrapher.Properties.Resources.CaptionSavedStrings, Calligrapher.Properties.Resources.MsgSavedStringsRTF);
		}
		Settings.Default.KeyboardLayoutIndex[((Selector)cmb_script).SelectedIndex] = ((Selector)cmb_keyboard).SelectedIndex.ToString();
		((SettingsBase)Settings.Default).Save();
		((Window)this).Close();
	}

	public void DoAction()
	{
		EnableDisableSaveButtons();
		if (UndoRedoActive)
		{
			return;
		}
		while (true)
		{
			switch (4)
			{
			case 0:
				continue;
			}
			if (1 == 0)
			{
				/*OpCode not supported: LdMemberToken*/;
			}
			UndoRedo.DoAction(MainCanvas.GetCanvasObjects());
			UpdateUndoRedo();
			return;
		}
	}

	private void UndoAction()
	{
		Mouse.OverrideCursor = Cursors.Wait;
		UndoRedoActive = (byte)_0019._0017(2104) != 0;
		RTFToolTip rTFToolTip = UndoRedo.UndoAction();
		if (rTFToolTip != null)
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
			MainCanvas.LoadCanvasObjects(DrawSettings, rTFToolTip.CanvasObjects);
		}
		UpdateUndoRedo();
		UpdatePreviewList((byte)_0019._0017(2108) != 0, null);
		EnableDisableSaveButtons();
		UndoRedoActive = (byte)_0019._0017(2112) != 0;
		Mouse.OverrideCursor = null;
	}

	private void RedoAction()
	{
		Mouse.OverrideCursor = Cursors.Wait;
		UndoRedoActive = (byte)_0019._0017(2116) != 0;
		RTFToolTip rTFToolTip = UndoRedo.RedoAction();
		if (rTFToolTip != null)
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
			if (1 == 0)
			{
				/*OpCode not supported: LdMemberToken*/;
			}
			MainCanvas.LoadCanvasObjects(DrawSettings, rTFToolTip.CanvasObjects);
		}
		UpdateUndoRedo();
		UpdatePreviewList((byte)_0019._0017(2120) != 0, null);
		EnableDisableSaveButtons();
		UndoRedoActive = (byte)_0019._0017(2124) != 0;
		Mouse.OverrideCursor = null;
	}

	private void UpdateUndoRedo()
	{
		if (UndoRedo.CanUndoAction())
		{
			((UIElement)Undo).IsEnabled = (byte)_0019._0017(2128) != 0;
		}
		else
		{
			((UIElement)Undo).IsEnabled = (byte)_0019._0017(2132) != 0;
		}
		if (UndoRedo.CanRedoAction())
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
					((UIElement)Redo).IsEnabled = (byte)_0019._0017(2136) != 0;
					return;
				}
			}
		}
		((UIElement)Redo).IsEnabled = (byte)_0019._0017(2140) != 0;
	}

	private void UpdatesNotification(bool available)
	{
		if (available)
		{
			((ContentControl)UpdatesToolTip).Content = _0011._0017(3180);
			UpdatesToolTip.PlacementTarget = (UIElement)(object)btn_checkupdate;
			UpdatesToolTip.Placement = (PlacementMode)_0019._0017(2144);
			UpdatesToolTip.VerticalOffset = _0019._0017(2148);
			UpdatesToolTip.IsOpen = (byte)_0019._0017(2156) != 0;
		}
		else
		{
			((ContentControl)UpdatesToolTip).Content = _0011._0017(3201);
			UpdatesToolTip.VerticalOffset = _0019._0017(2160);
			UpdatesToolTip.Placement = (PlacementMode)_0019._0017(2168);
			UpdatesToolTip.PlacementTarget = (UIElement)(object)btn_checkupdate;
			UpdatesToolTip.IsOpen = (byte)_0019._0017(2172) != 0;
		}
	}

	private void AutoUpdatesTimer_Tick(object sender, EventArgs e)
	{
		//IL_0049: Unknown result type (might be due to invalid IL or missing references)
		//IL_004e: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (IsDemo)
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
				if (1 == 0)
				{
					/*OpCode not supported: LdMemberToken*/;
				}
				UpdatesManager.DisplayUpdatesNotification(UpdatesNotification);
				return;
			}
		}
		catch (SLCNetworkException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void StartUpdatesTimer_Tick(object sender, EventArgs e)
	{
		//IL_0041: Unknown result type (might be due to invalid IL or missing references)
		//IL_0046: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			if (!IsDemo)
			{
				UpdatesManager.DisplayUpdatesNotification(UpdatesNotification);
				StartUpdatesTimer.Stop();
			}
		}
		catch (SLCNetworkException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void LicensingTimer_Tick(object sender, EventArgs e)
	{
		//IL_0012: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		//IL_014e: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00eb: Unknown result type (might be due to invalid IL or missing references)
		//IL_0129: Unknown result type (might be due to invalid IL or missing references)
		//IL_012e: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			string text = "";
			string text2 = "";
			RegistryHelper val = new RegistryHelper(IsDemo);
			if (val == null)
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
				GObjects.Log.GTLogDebugMsg(_0011._0017(2098));
			}
			PIKNIK instance = PIKNIK.GetInstance((Type)_0019._0017(2176), val.GetAppInstallPath());
			if (instance != null)
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
				if (instance.PIKNIK2())
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
					instance.PIKNIK8((PIKNIKE)_0019._0017(2180), ref text, (byte)_0019._0017(2184) != 0);
					text2 = GObjects.LM.SLM3();
					CES.CES2(text2, ref text2);
				}
				else
				{
					GObjects.Log.GTLogDebugMsg(_0011._0017(2135));
				}
			}
			if (text != text2)
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
				GObjects.Message.ShowErrorSendLogs(Calligrapher.Properties.Resources.MsgLicense);
				((Window)this).Close();
			}
			if (GObjects.LM.SLM11() == _0019._0017(2188))
			{
				while (true)
				{
					switch (1)
					{
					case 0:
						break;
					default:
						IsDemo = (byte)_0019._0017(2192) != 0;
						GObjects.Message.ShowErrorDemoVersion();
						return;
					}
				}
			}
			IsDemo = (byte)_0019._0017(2196) != 0;
		}
		catch (Exception ex)
		{
			GObjects.Message.ShowErrorGeneric(ex);
		}
	}

	private void PromotionsTimer_Tick(object sender, EventArgs e)
	{
		//IL_005f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0064: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			PromotionsManager.DisplayPromotionsNotification();
			PromotionsTimer.Interval = new TimeSpan(Settings.Default.TimerPromotions / _0019._0017(2200), _0019._0017(2204), _0019._0017(2208));
		}
		catch (SLCNetworkException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void UserAnalyticsTimer_Tick(object sender, EventArgs e)
	{
		//IL_0095: Unknown result type (might be due to invalid IL or missing references)
		//IL_009a: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			string text = SLCFileType.ToString(RecentCollection);
			if (text.Length > _0019._0017(2212))
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
				UserAnalyticsManager.SendAnalytics(text);
			}
			UserAnalyticsTimer.Interval = new TimeSpan(Settings.Default.TimerUserAnalytics / _0019._0017(2216), _0019._0017(2220), _0019._0017(2224));
		}
		catch (SLCNetworkException ex)
		{
			GObjects.Log.GTLogException((Exception)ex);
		}
		catch (Exception ex2)
		{
			GObjects.Message.ShowErrorGeneric(ex2);
		}
	}

	private void PopupTimer_Tick(object sender, EventArgs e)
	{
		t2ToolTip.IsOpen = (byte)_0019._0017(2228) != 0;
		PopupTimer.Stop();
	}

	[DebuggerNonUserCode]
	[GeneratedCode("PresentationBuildTasks", "4.0.0.0")]
	public void InitializeComponent()
	{
		if (!_contentLoaded)
		{
			_contentLoaded = (byte)_0019._0017(2232) != 0;
			Uri uri = new Uri(_0011._0017(3236), (UriKind)_0019._0017(2236));
			Application.LoadComponent((object)this, uri);
		}
	}

	[DebuggerNonUserCode]
	[GeneratedCode("PresentationBuildTasks", "4.0.0.0")]
	internal Delegate _CreateDelegate(Type delegateType, string handler)
	{
		return Delegate.CreateDelegate(delegateType, this, handler);
	}

	[GeneratedCode("PresentationBuildTasks", "4.0.0.0")]
	[DebuggerNonUserCode]
	[EditorBrowsable(EditorBrowsableState.Never)]
	void IComponentConnector.Connect(int connectionId, object target)
	{
		//IL_00c0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ca: Expected O, but got Unknown
		//IL_00cd: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d7: Expected O, but got Unknown
		//IL_00da: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e4: Expected O, but got Unknown
		//IL_00f1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fb: Expected O, but got Unknown
		//IL_00fe: Unknown result type (might be due to invalid IL or missing references)
		//IL_0108: Expected O, but got Unknown
		//IL_0115: Unknown result type (might be due to invalid IL or missing references)
		//IL_011f: Expected O, but got Unknown
		//IL_0122: Unknown result type (might be due to invalid IL or missing references)
		//IL_012c: Expected O, but got Unknown
		//IL_0139: Unknown result type (might be due to invalid IL or missing references)
		//IL_0143: Expected O, but got Unknown
		//IL_0146: Unknown result type (might be due to invalid IL or missing references)
		//IL_0150: Expected O, but got Unknown
		//IL_015d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0167: Expected O, but got Unknown
		//IL_016a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0174: Expected O, but got Unknown
		//IL_0181: Unknown result type (might be due to invalid IL or missing references)
		//IL_018b: Expected O, but got Unknown
		//IL_018e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0198: Expected O, but got Unknown
		//IL_01a5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01af: Expected O, but got Unknown
		//IL_01b2: Unknown result type (might be due to invalid IL or missing references)
		//IL_01bc: Expected O, but got Unknown
		//IL_01c9: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d3: Expected O, but got Unknown
		//IL_01d6: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e0: Expected O, but got Unknown
		//IL_01ed: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f7: Expected O, but got Unknown
		//IL_01fa: Unknown result type (might be due to invalid IL or missing references)
		//IL_0204: Expected O, but got Unknown
		//IL_0211: Unknown result type (might be due to invalid IL or missing references)
		//IL_021b: Expected O, but got Unknown
		//IL_021e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0228: Expected O, but got Unknown
		//IL_0235: Unknown result type (might be due to invalid IL or missing references)
		//IL_023f: Expected O, but got Unknown
		//IL_0242: Unknown result type (might be due to invalid IL or missing references)
		//IL_024c: Expected O, but got Unknown
		//IL_0259: Unknown result type (might be due to invalid IL or missing references)
		//IL_0263: Expected O, but got Unknown
		//IL_0266: Unknown result type (might be due to invalid IL or missing references)
		//IL_0270: Expected O, but got Unknown
		//IL_027d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0287: Expected O, but got Unknown
		//IL_028a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0294: Expected O, but got Unknown
		//IL_02a1: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ab: Expected O, but got Unknown
		//IL_02ae: Unknown result type (might be due to invalid IL or missing references)
		//IL_02b8: Expected O, but got Unknown
		//IL_02bb: Unknown result type (might be due to invalid IL or missing references)
		//IL_02c5: Expected O, but got Unknown
		//IL_02d2: Unknown result type (might be due to invalid IL or missing references)
		//IL_02dc: Expected O, but got Unknown
		//IL_02df: Unknown result type (might be due to invalid IL or missing references)
		//IL_02e9: Expected O, but got Unknown
		//IL_02f6: Unknown result type (might be due to invalid IL or missing references)
		//IL_0300: Expected O, but got Unknown
		//IL_0303: Unknown result type (might be due to invalid IL or missing references)
		//IL_030d: Expected O, but got Unknown
		//IL_0310: Unknown result type (might be due to invalid IL or missing references)
		//IL_031a: Expected O, but got Unknown
		//IL_032a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0334: Expected O, but got Unknown
		//IL_0337: Unknown result type (might be due to invalid IL or missing references)
		//IL_0341: Expected O, but got Unknown
		//IL_0344: Unknown result type (might be due to invalid IL or missing references)
		//IL_034e: Expected O, but got Unknown
		//IL_0351: Unknown result type (might be due to invalid IL or missing references)
		//IL_035b: Expected O, but got Unknown
		//IL_0368: Unknown result type (might be due to invalid IL or missing references)
		//IL_0372: Expected O, but got Unknown
		//IL_037f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0389: Expected O, but got Unknown
		//IL_0396: Unknown result type (might be due to invalid IL or missing references)
		//IL_03a0: Expected O, but got Unknown
		//IL_03a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_03ad: Expected O, but got Unknown
		//IL_03b0: Unknown result type (might be due to invalid IL or missing references)
		//IL_03ba: Expected O, but got Unknown
		//IL_03bd: Unknown result type (might be due to invalid IL or missing references)
		//IL_03c7: Expected O, but got Unknown
		//IL_03d4: Unknown result type (might be due to invalid IL or missing references)
		//IL_03de: Expected O, but got Unknown
		//IL_03e1: Unknown result type (might be due to invalid IL or missing references)
		//IL_03eb: Expected O, but got Unknown
		//IL_03ee: Unknown result type (might be due to invalid IL or missing references)
		//IL_03f8: Expected O, but got Unknown
		//IL_0405: Unknown result type (might be due to invalid IL or missing references)
		//IL_040f: Expected O, but got Unknown
		//IL_041c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0426: Expected O, but got Unknown
		//IL_0429: Unknown result type (might be due to invalid IL or missing references)
		//IL_0433: Expected O, but got Unknown
		switch (connectionId - _0019._0017(2240))
		{
		case 0:
			AppWindow = (MainWindow)target;
			((Window)AppWindow).Closed += Window_Closed;
			break;
		case 1:
			MainGrid = (Grid)target;
			break;
		case 2:
			MainDockPanel = (DockPanel)target;
			break;
		case 3:
			cmb_script = (ComboBox)target;
			((Selector)cmb_script).SelectionChanged += new SelectionChangedEventHandler(cmb_script_SelectionChanged);
			break;
		case 4:
			cmb_Font = (ComboBox)target;
			((Selector)cmb_Font).SelectionChanged += new SelectionChangedEventHandler(cmb_Font_SelectionChanged);
			break;
		case 5:
			cmb_keyboard = (ComboBox)target;
			((Selector)cmb_keyboard).SelectionChanged += new SelectionChangedEventHandler(cmb_keyboard_SelectionChanged);
			break;
		case 6:
			btnNew = (Button)target;
			((ButtonBase)btnNew).Click += new RoutedEventHandler(btnNew_Click);
			break;
		case 7:
			btnOpen = (Button)target;
			((ButtonBase)btnOpen).Click += new RoutedEventHandler(btnOpen_Click);
			break;
		case 8:
			btnSave = (Button)target;
			((ButtonBase)btnSave).Click += new RoutedEventHandler(btnSave_Click);
			break;
		case 9:
			btnExport = (Button)target;
			((ButtonBase)btnExport).Click += new RoutedEventHandler(btnExport_Click);
			break;
		case 10:
			Undo = (Button)target;
			((ButtonBase)Undo).Click += new RoutedEventHandler(Undo_Click);
			break;
		case 11:
			Redo = (Button)target;
			((ButtonBase)Redo).Click += new RoutedEventHandler(Redo_Click);
			break;
		case 12:
			btn_Settings = (Button)target;
			((ButtonBase)btn_Settings).Click += new RoutedEventHandler(btn_Settings_Click);
			break;
		case 13:
			btnTutor = (ToggleButton)target;
			((ButtonBase)btnTutor).Click += new RoutedEventHandler(btnTutor_Click);
			break;
		case 14:
			btn_lnk = (Button)target;
			((ButtonBase)btn_lnk).Click += new RoutedEventHandler(btn_lnk_Click);
			break;
		case 15:
			btn_checkupdate = (Button)target;
			((ButtonBase)btn_checkupdate).Click += new RoutedEventHandler(btn_checkupdate_Click);
			break;
		case 16:
			UpdatesToolTip = (ToolTip)target;
			break;
		case 17:
			btn_Help = (Button)target;
			((ButtonBase)btn_Help).Click += new RoutedEventHandler(btn_Help_Click);
			break;
		case 18:
			btn_About = (Button)target;
			((ButtonBase)btn_About).Click += new RoutedEventHandler(btn_About_Click);
			break;
		case 19:
			ContentGrid = (Grid)target;
			break;
		case 20:
			CanvasPanel = (DockPanel)target;
			break;
		case 21:
			MainCanvas = (DragCanvas)target;
			break;
		case 22:
			TabPreviewRecent = (TabControl)target;
			break;
		case 23:
			t1 = (TabItem)target;
			break;
		case 24:
			t1Container = (DockPanel)target;
			break;
		case 25:
			lst_Preview = (ListBox)target;
			((Control)lst_Preview).MouseDoubleClick += new MouseButtonEventHandler(lst_Preview_MouseDoubleClick);
			((Selector)lst_Preview).SelectionChanged += new SelectionChangedEventHandler(lst_Preview_SelectionChanged);
			((UIElement)lst_Preview).KeyUp += new KeyEventHandler(lst_Preview_KeyUp);
			break;
		case 26:
			t2 = (TabItem)target;
			break;
		case 27:
			t2ToolTip = (ToolTip)target;
			break;
		case 28:
			btnClearAllQuicksave = (Button)target;
			((ButtonBase)btnClearAllQuicksave).Click += new RoutedEventHandler(btnClearAllQuicksave_Click);
			break;
		case 29:
			t2Container = (DockPanel)target;
			break;
		case 30:
			lst_Recent = (ListBox)target;
			((Control)lst_Recent).MouseDoubleClick += new MouseButtonEventHandler(lst_Recent_MouseDoubleClick);
			((UIElement)lst_Recent).KeyUp += new KeyEventHandler(lst_Recent_KeyUp);
			break;
		case 32:
			KBTutor = (FloatingTouchScreenKeyboard)target;
			break;
		default:
			_contentLoaded = (byte)_0019._0017(2244) != 0;
			break;
		}
	}

	[EditorBrowsable(EditorBrowsableState.Never)]
	[GeneratedCode("PresentationBuildTasks", "4.0.0.0")]
	[DebuggerNonUserCode]
	void IStyleConnector.Connect(int connectionId, object target)
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_001a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0024: Expected O, but got Unknown
		if (connectionId == _0019._0017(2248))
		{
			((ButtonBase)(Button)target).Click += new RoutedEventHandler(btnRemoveQuickSave_Click);
		}
	}
}
