%General Mission Analysis Tool(GMAT) Script
%Created: 2022-04-02 15:31:59


%----------------------------------------
%---------- Spacecraft
%----------------------------------------

Create Spacecraft GEO1;
GMAT GEO1.DateFormat = TAIModJulian;
GMAT GEO1.Epoch = '21545';
GMAT GEO1.CoordinateSystem = EarthMJ2000Eq;
GMAT GEO1.DisplayStateType = Keplerian;
GMAT GEO1.SMA = 42165.00000000002;
GMAT GEO1.ECC = 9.395384241353323e-16;
GMAT GEO1.INC = 27;
GMAT GEO1.RAAN = 0;
GMAT GEO1.AOP = 0;
GMAT GEO1.TA = 0;
GMAT GEO1.DryMass = 850;
GMAT GEO1.Cd = 2.2;
GMAT GEO1.Cr = 1.8;
GMAT GEO1.DragArea = 15;
GMAT GEO1.SRPArea = 1;
GMAT GEO1.SPADDragScaleFactor = 1;
GMAT GEO1.SPADSRPScaleFactor = 1;
GMAT GEO1.NAIFId = -10001001;
GMAT GEO1.NAIFIdReferenceFrame = -9001001;
GMAT GEO1.OrbitColor = Red;
GMAT GEO1.TargetColor = Teal;
GMAT GEO1.OrbitErrorCovariance = [ 1e+70 0 0 0 0 0 ; 0 1e+70 0 0 0 0 ; 0 0 1e+70 0 0 0 ; 0 0 0 1e+70 0 0 ; 0 0 0 0 1e+70 0 ; 0 0 0 0 0 1e+70 ];
GMAT GEO1.CdSigma = 1e+70;
GMAT GEO1.CrSigma = 1e+70;
GMAT GEO1.Id = 'SatId';
GMAT GEO1.Attitude = CoordinateSystemFixed;
GMAT GEO1.SPADSRPInterpolationMethod = Bilinear;
GMAT GEO1.SPADSRPScaleFactorSigma = 1e+70;
GMAT GEO1.SPADDragInterpolationMethod = Bilinear;
GMAT GEO1.SPADDragScaleFactorSigma = 1e+70;
GMAT GEO1.ModelFile = 'aura.3ds';
GMAT GEO1.ModelOffsetX = 0;
GMAT GEO1.ModelOffsetY = 0;
GMAT GEO1.ModelOffsetZ = 0;
GMAT GEO1.ModelRotationX = 0;
GMAT GEO1.ModelRotationY = 0;
GMAT GEO1.ModelRotationZ = 0;
GMAT GEO1.ModelScale = 1;
GMAT GEO1.AttitudeDisplayStateType = 'Quaternion';
GMAT GEO1.AttitudeRateDisplayStateType = 'AngularVelocity';
GMAT GEO1.AttitudeCoordinateSystem = EarthMJ2000Eq;
GMAT GEO1.EulerAngleSequence = '321';

%----------------------------------------
%---------- Spacecraft
%----------------------------------------

Create Spacecraft GEO2;
GMAT GEO2.DateFormat = TAIModJulian;
GMAT GEO2.Epoch = '21545';
GMAT GEO2.CoordinateSystem = EarthMJ2000Eq;
GMAT GEO2.DisplayStateType = Keplerian;
GMAT GEO2.SMA = 42165.00000000003;
GMAT GEO2.ECC = 6.05178359332816e-16;
GMAT GEO2.INC = 27;
GMAT GEO2.RAAN = 120;
GMAT GEO2.AOP = 0;
GMAT GEO2.TA = 240;
GMAT GEO2.DryMass = 850;
GMAT GEO2.Cd = 2.2;
GMAT GEO2.Cr = 1.8;
GMAT GEO2.DragArea = 15;
GMAT GEO2.SRPArea = 1;
GMAT GEO2.SPADDragScaleFactor = 1;
GMAT GEO2.SPADSRPScaleFactor = 1;
GMAT GEO2.NAIFId = -10001001;
GMAT GEO2.NAIFIdReferenceFrame = -9001001;
GMAT GEO2.OrbitColor = Red;
GMAT GEO2.TargetColor = Teal;
GMAT GEO2.OrbitErrorCovariance = [ 1e+70 0 0 0 0 0 ; 0 1e+70 0 0 0 0 ; 0 0 1e+70 0 0 0 ; 0 0 0 1e+70 0 0 ; 0 0 0 0 1e+70 0 ; 0 0 0 0 0 1e+70 ];
GMAT GEO2.CdSigma = 1e+70;
GMAT GEO2.CrSigma = 1e+70;
GMAT GEO2.Id = 'SatId';
GMAT GEO2.Attitude = CoordinateSystemFixed;
GMAT GEO2.SPADSRPInterpolationMethod = Bilinear;
GMAT GEO2.SPADSRPScaleFactorSigma = 1e+70;
GMAT GEO2.SPADDragInterpolationMethod = Bilinear;
GMAT GEO2.SPADDragScaleFactorSigma = 1e+70;
GMAT GEO2.ModelFile = 'aura.3ds';
GMAT GEO2.ModelOffsetX = 0;
GMAT GEO2.ModelOffsetY = 0;
GMAT GEO2.ModelOffsetZ = 0;
GMAT GEO2.ModelRotationX = 0;
GMAT GEO2.ModelRotationY = 0;
GMAT GEO2.ModelRotationZ = 0;
GMAT GEO2.ModelScale = 1;
GMAT GEO2.AttitudeDisplayStateType = 'Quaternion';
GMAT GEO2.AttitudeRateDisplayStateType = 'AngularVelocity';
GMAT GEO2.AttitudeCoordinateSystem = EarthMJ2000Eq;
GMAT GEO2.EulerAngleSequence = '321';

%----------------------------------------
%---------- Spacecraft
%----------------------------------------

Create Spacecraft GEO3;
GMAT GEO3.DateFormat = TAIModJulian;
GMAT GEO3.Epoch = '21545';
GMAT GEO3.CoordinateSystem = EarthMJ2000Eq;
GMAT GEO3.DisplayStateType = Keplerian;
GMAT GEO3.SMA = 42165.00000000001;
GMAT GEO3.ECC = 7.296062955109464e-16;
GMAT GEO3.INC = 27;
GMAT GEO3.RAAN = 239.9999999999999;
GMAT GEO3.AOP = 0;
GMAT GEO3.TA = 120;
GMAT GEO3.DryMass = 850;
GMAT GEO3.Cd = 2.2;
GMAT GEO3.Cr = 1.8;
GMAT GEO3.DragArea = 15;
GMAT GEO3.SRPArea = 1;
GMAT GEO3.SPADDragScaleFactor = 1;
GMAT GEO3.SPADSRPScaleFactor = 1;
GMAT GEO3.NAIFId = -10001001;
GMAT GEO3.NAIFIdReferenceFrame = -9001001;
GMAT GEO3.OrbitColor = Red;
GMAT GEO3.TargetColor = Teal;
GMAT GEO3.OrbitErrorCovariance = [ 1e+70 0 0 0 0 0 ; 0 1e+70 0 0 0 0 ; 0 0 1e+70 0 0 0 ; 0 0 0 1e+70 0 0 ; 0 0 0 0 1e+70 0 ; 0 0 0 0 0 1e+70 ];
GMAT GEO3.CdSigma = 1e+70;
GMAT GEO3.CrSigma = 1e+70;
GMAT GEO3.Id = 'SatId';
GMAT GEO3.Attitude = CoordinateSystemFixed;
GMAT GEO3.SPADSRPInterpolationMethod = Bilinear;
GMAT GEO3.SPADSRPScaleFactorSigma = 1e+70;
GMAT GEO3.SPADDragInterpolationMethod = Bilinear;
GMAT GEO3.SPADDragScaleFactorSigma = 1e+70;
GMAT GEO3.ModelFile = 'aura.3ds';
GMAT GEO3.ModelOffsetX = 0;
GMAT GEO3.ModelOffsetY = 0;
GMAT GEO3.ModelOffsetZ = 0;
GMAT GEO3.ModelRotationX = 0;
GMAT GEO3.ModelRotationY = 0;
GMAT GEO3.ModelRotationZ = 0;
GMAT GEO3.ModelScale = 1;
GMAT GEO3.AttitudeDisplayStateType = 'Quaternion';
GMAT GEO3.AttitudeRateDisplayStateType = 'AngularVelocity';
GMAT GEO3.AttitudeCoordinateSystem = EarthMJ2000Eq;
GMAT GEO3.EulerAngleSequence = '321';

%----------------------------------------
%---------- GroundStations
%----------------------------------------

Create GroundStation AshmoreIslands;
GMAT AshmoreIslands.OrbitColor = Thistle;
GMAT AshmoreIslands.TargetColor = [252 102 101];
GMAT AshmoreIslands.CentralBody = Earth;
GMAT AshmoreIslands.StateType = Spherical;
GMAT AshmoreIslands.HorizonReference = Sphere;
GMAT AshmoreIslands.Location1 = -12.183;
GMAT AshmoreIslands.Location2 = 122.983;
GMAT AshmoreIslands.Location3 = 0;
GMAT AshmoreIslands.Id = 'Ashmore';
GMAT AshmoreIslands.IonosphereModel = 'None';
GMAT AshmoreIslands.TroposphereModel = 'None';
GMAT AshmoreIslands.DataSource = 'Constant';
GMAT AshmoreIslands.Temperature = 295.1;
GMAT AshmoreIslands.Pressure = 1013.5;
GMAT AshmoreIslands.Humidity = 55;
GMAT AshmoreIslands.MinimumElevationAngle = 20;

Create GroundStation CartierIsland;
GMAT CartierIsland.OrbitColor = Thistle;
GMAT CartierIsland.TargetColor = [253 204 101];
GMAT CartierIsland.CentralBody = Earth;
GMAT CartierIsland.StateType = Spherical;
GMAT CartierIsland.HorizonReference = Sphere;
GMAT CartierIsland.Location1 = -12.51;
GMAT CartierIsland.Location2 = 123.55;
GMAT CartierIsland.Location3 = 0;
GMAT CartierIsland.Id = 'Cartier';
GMAT CartierIsland.IonosphereModel = 'None';
GMAT CartierIsland.TroposphereModel = 'None';
GMAT CartierIsland.DataSource = 'Constant';
GMAT CartierIsland.Temperature = 295.1;
GMAT CartierIsland.Pressure = 1013.5;
GMAT CartierIsland.Humidity = 55;
GMAT CartierIsland.MinimumElevationAngle = 20;

Create GroundStation CaseyStation;
GMAT CaseyStation.OrbitColor = Thistle;
GMAT CaseyStation.TargetColor = [254 255 102];
GMAT CaseyStation.CentralBody = Earth;
GMAT CaseyStation.StateType = Spherical;
GMAT CaseyStation.HorizonReference = Sphere;
GMAT CaseyStation.Location1 = -66.28;
GMAT CaseyStation.Location2 = 110.53;
GMAT CaseyStation.Location3 = 0;
GMAT CaseyStation.Id = 'StationId';
GMAT CaseyStation.IonosphereModel = 'None';
GMAT CaseyStation.TroposphereModel = 'None';
GMAT CaseyStation.DataSource = 'Constant';
GMAT CaseyStation.Temperature = 295.1;
GMAT CaseyStation.Pressure = 1013.5;
GMAT CaseyStation.Humidity = 55;
GMAT CaseyStation.MinimumElevationAngle = 20;

Create GroundStation DavisStation;
GMAT DavisStation.OrbitColor = Thistle;
GMAT DavisStation.TargetColor = [203 255 102];
GMAT DavisStation.CentralBody = Earth;
GMAT DavisStation.StateType = Spherical;
GMAT DavisStation.HorizonReference = Sphere;
GMAT DavisStation.Location1 = -68.583;
GMAT DavisStation.Location2 = 77.967;
GMAT DavisStation.Location3 = 0;
GMAT DavisStation.Id = 'StationId';
GMAT DavisStation.IonosphereModel = 'None';
GMAT DavisStation.TroposphereModel = 'None';
GMAT DavisStation.DataSource = 'Constant';
GMAT DavisStation.Temperature = 295.1;
GMAT DavisStation.Pressure = 1013.5;
GMAT DavisStation.Humidity = 55;
GMAT DavisStation.MinimumElevationAngle = 20;

Create GroundStation MawsonStation;
GMAT MawsonStation.OrbitColor = Thistle;
GMAT MawsonStation.TargetColor = [101 255 102];
GMAT MawsonStation.CentralBody = Earth;
GMAT MawsonStation.StateType = Spherical;
GMAT MawsonStation.HorizonReference = Sphere;
GMAT MawsonStation.Location1 = -67.59999999999999;
GMAT MawsonStation.Location2 = 62.867;
GMAT MawsonStation.Location3 = 0;
GMAT MawsonStation.Id = 'StationId';
GMAT MawsonStation.IonosphereModel = 'None';
GMAT MawsonStation.TroposphereModel = 'None';
GMAT MawsonStation.DataSource = 'Constant';
GMAT MawsonStation.Temperature = 295.1;
GMAT MawsonStation.Pressure = 1013.5;
GMAT MawsonStation.Humidity = 55;
GMAT MawsonStation.MinimumElevationAngle = 20;

Create GroundStation MacquarieStation;
GMAT MacquarieStation.OrbitColor = Thistle;
GMAT MacquarieStation.TargetColor = [101 255 204];
GMAT MacquarieStation.CentralBody = Earth;
GMAT MacquarieStation.StateType = Spherical;
GMAT MacquarieStation.HorizonReference = Sphere;
GMAT MacquarieStation.Location1 = -54.5;
GMAT MacquarieStation.Location2 = 158.95;
GMAT MacquarieStation.Location3 = 0;
GMAT MacquarieStation.Id = 'StationId';
GMAT MacquarieStation.IonosphereModel = 'None';
GMAT MacquarieStation.TroposphereModel = 'None';
GMAT MacquarieStation.DataSource = 'Constant';
GMAT MacquarieStation.Temperature = 295.1;
GMAT MacquarieStation.Pressure = 1013.5;
GMAT MacquarieStation.Humidity = 55;
GMAT MacquarieStation.MinimumElevationAngle = 20;

Create GroundStation ChristmasIsland;
GMAT ChristmasIsland.OrbitColor = Thistle;
GMAT ChristmasIsland.TargetColor = [101 255 254];
GMAT ChristmasIsland.CentralBody = Earth;
GMAT ChristmasIsland.StateType = Spherical;
GMAT ChristmasIsland.HorizonReference = Sphere;
GMAT ChristmasIsland.Location1 = -10.41;
GMAT ChristmasIsland.Location2 = 105.716;
GMAT ChristmasIsland.Location3 = 0;
GMAT ChristmasIsland.Id = 'ChristmasIsland';
GMAT ChristmasIsland.IonosphereModel = 'None';
GMAT ChristmasIsland.TroposphereModel = 'None';
GMAT ChristmasIsland.DataSource = 'Constant';
GMAT ChristmasIsland.Temperature = 295.1;
GMAT ChristmasIsland.Pressure = 1013.5;
GMAT ChristmasIsland.Humidity = 55;
GMAT ChristmasIsland.MinimumElevationAngle = 20;

Create GroundStation CocosIslands;
GMAT CocosIslands.OrbitColor = Thistle;
GMAT CocosIslands.TargetColor = [101 204 254];
GMAT CocosIslands.CentralBody = Earth;
GMAT CocosIslands.StateType = Spherical;
GMAT CocosIslands.HorizonReference = Sphere;
GMAT CocosIslands.Location1 = -12.167;
GMAT CocosIslands.Location2 = 96.833;
GMAT CocosIslands.Location3 = 0;
GMAT CocosIslands.Id = 'StationId';
GMAT CocosIslands.IonosphereModel = 'None';
GMAT CocosIslands.TroposphereModel = 'None';
GMAT CocosIslands.DataSource = 'Constant';
GMAT CocosIslands.Temperature = 295.1;
GMAT CocosIslands.Pressure = 1013.5;
GMAT CocosIslands.Humidity = 55;
GMAT CocosIslands.MinimumElevationAngle = 20;

Create GroundStation CoralSeaIslands;
GMAT CoralSeaIslands.OrbitColor = Thistle;
GMAT CoralSeaIslands.TargetColor = [102 102 254];
GMAT CoralSeaIslands.CentralBody = Earth;
GMAT CoralSeaIslands.StateType = Spherical;
GMAT CoralSeaIslands.HorizonReference = Sphere;
GMAT CoralSeaIslands.Location1 = -23.25;
GMAT CoralSeaIslands.Location2 = 155.533;
GMAT CoralSeaIslands.Location3 = 0;
GMAT CoralSeaIslands.Id = 'StationId';
GMAT CoralSeaIslands.IonosphereModel = 'None';
GMAT CoralSeaIslands.TroposphereModel = 'None';
GMAT CoralSeaIslands.DataSource = 'Constant';
GMAT CoralSeaIslands.Temperature = 295.1;
GMAT CoralSeaIslands.Pressure = 1013.5;
GMAT CoralSeaIslands.Humidity = 55;
GMAT CoralSeaIslands.MinimumElevationAngle = 20;

Create GroundStation HeardMcDonaldIslands;
GMAT HeardMcDonaldIslands.OrbitColor = Thistle;
GMAT HeardMcDonaldIslands.TargetColor = [204 102 254];
GMAT HeardMcDonaldIslands.CentralBody = Earth;
GMAT HeardMcDonaldIslands.StateType = Spherical;
GMAT HeardMcDonaldIslands.HorizonReference = Sphere;
GMAT HeardMcDonaldIslands.Location1 = -53.08333;
GMAT HeardMcDonaldIslands.Location2 = 73.5;
GMAT HeardMcDonaldIslands.Location3 = 0;
GMAT HeardMcDonaldIslands.Id = 'StationId';
GMAT HeardMcDonaldIslands.IonosphereModel = 'None';
GMAT HeardMcDonaldIslands.TroposphereModel = 'None';
GMAT HeardMcDonaldIslands.DataSource = 'Constant';
GMAT HeardMcDonaldIslands.Temperature = 295.1;
GMAT HeardMcDonaldIslands.Pressure = 1013.5;
GMAT HeardMcDonaldIslands.Humidity = 55;
GMAT HeardMcDonaldIslands.MinimumElevationAngle = 20;

Create GroundStation NorfolkIsland;
GMAT NorfolkIsland.OrbitColor = Thistle;
GMAT NorfolkIsland.TargetColor = [252 102 254];
GMAT NorfolkIsland.CentralBody = Earth;
GMAT NorfolkIsland.StateType = Spherical;
GMAT NorfolkIsland.HorizonReference = Sphere;
GMAT NorfolkIsland.Location1 = -29.033;
GMAT NorfolkIsland.Location2 = 167.95;
GMAT NorfolkIsland.Location3 = 0;
GMAT NorfolkIsland.Id = 'StationId';
GMAT NorfolkIsland.IonosphereModel = 'None';
GMAT NorfolkIsland.TroposphereModel = 'None';
GMAT NorfolkIsland.DataSource = 'Constant';
GMAT NorfolkIsland.Temperature = 295.1;
GMAT NorfolkIsland.Pressure = 1013.5;
GMAT NorfolkIsland.Humidity = 55;
GMAT NorfolkIsland.MinimumElevationAngle = 20;








%----------------------------------------
%---------- ForceModels
%----------------------------------------

Create ForceModel DefaultProp_ForceModel;
GMAT DefaultProp_ForceModel.CentralBody = Earth;
GMAT DefaultProp_ForceModel.PrimaryBodies = {Earth};
GMAT DefaultProp_ForceModel.Drag = None;
GMAT DefaultProp_ForceModel.SRP = Off;
GMAT DefaultProp_ForceModel.RelativisticCorrection = Off;
GMAT DefaultProp_ForceModel.ErrorControl = RSSStep;
GMAT DefaultProp_ForceModel.GravityField.Earth.Degree = 4;
GMAT DefaultProp_ForceModel.GravityField.Earth.Order = 4;
GMAT DefaultProp_ForceModel.GravityField.Earth.StmLimit = 100;
GMAT DefaultProp_ForceModel.GravityField.Earth.PotentialFile = 'JGM2.cof';
GMAT DefaultProp_ForceModel.GravityField.Earth.TideModel = 'None';

%----------------------------------------
%---------- Propagators
%----------------------------------------

Create Propagator DefaultProp;
GMAT DefaultProp.FM = DefaultProp_ForceModel;
GMAT DefaultProp.Type = RungeKutta89;
GMAT DefaultProp.InitialStepSize = 60;
GMAT DefaultProp.Accuracy = 9.999999999999999e-12;
GMAT DefaultProp.MinStep = 0.001;
GMAT DefaultProp.MaxStep = 2700;
GMAT DefaultProp.MaxStepAttempts = 50;
GMAT DefaultProp.StopIfAccuracyIsViolated = true;

%----------------------------------------
%---------- EventLocators
%----------------------------------------

Create ContactLocator ContactLocator1;
GMAT ContactLocator1.Target = GEO1;
GMAT ContactLocator1.Filename = 'ContactLocator1.txt';
GMAT ContactLocator1.InputEpochFormat = 'TAIModJulian';
GMAT ContactLocator1.InitialEpoch = '21545';
GMAT ContactLocator1.StepSize = 10;
GMAT ContactLocator1.FinalEpoch = '21545.138';
GMAT ContactLocator1.UseLightTimeDelay = true;
GMAT ContactLocator1.UseStellarAberration = true;
GMAT ContactLocator1.WriteReport = true;
GMAT ContactLocator1.RunMode = Automatic;
GMAT ContactLocator1.UseEntireInterval = true;
GMAT ContactLocator1.Observers = {AshmoreIslands, CartierIsland, CaseyStation, ChristmasIsland, CocosIslands, CoralSeaIslands, DavisStation, HeardMcDonaldIslands, MacquarieStation, MawsonStation, NorfolkIsland};
GMAT ContactLocator1.LightTimeDirection = Transmit;

Create ContactLocator ContactLocator2;
GMAT ContactLocator2.Target = GEO2;
GMAT ContactLocator2.Filename = 'ContactLocator2.txt';
GMAT ContactLocator2.InputEpochFormat = 'TAIModJulian';
GMAT ContactLocator2.InitialEpoch = '21545';
GMAT ContactLocator2.StepSize = 10;
GMAT ContactLocator2.FinalEpoch = '21545.138';
GMAT ContactLocator2.UseLightTimeDelay = true;
GMAT ContactLocator2.UseStellarAberration = true;
GMAT ContactLocator2.WriteReport = true;
GMAT ContactLocator2.RunMode = Automatic;
GMAT ContactLocator2.UseEntireInterval = true;
GMAT ContactLocator2.Observers = {AshmoreIslands, CartierIsland, CaseyStation, ChristmasIsland, CocosIslands, CoralSeaIslands, DavisStation, HeardMcDonaldIslands, MacquarieStation, MawsonStation, NorfolkIsland};
GMAT ContactLocator2.LightTimeDirection = Transmit;

Create ContactLocator ContactLocator3;
GMAT ContactLocator3.Target = GEO3;
GMAT ContactLocator3.Filename = 'ContactLocator3.txt';
GMAT ContactLocator3.InputEpochFormat = 'TAIModJulian';
GMAT ContactLocator3.InitialEpoch = '21545';
GMAT ContactLocator3.StepSize = 10;
GMAT ContactLocator3.FinalEpoch = '21545.138';
GMAT ContactLocator3.UseLightTimeDelay = true;
GMAT ContactLocator3.UseStellarAberration = true;
GMAT ContactLocator3.WriteReport = true;
GMAT ContactLocator3.RunMode = Automatic;
GMAT ContactLocator3.UseEntireInterval = true;
GMAT ContactLocator3.Observers = {AshmoreIslands, CartierIsland, CaseyStation, ChristmasIsland, CocosIslands, CoralSeaIslands, DavisStation, HeardMcDonaldIslands, MacquarieStation, MawsonStation, NorfolkIsland};
GMAT ContactLocator3.LightTimeDirection = Transmit;

%----------------------------------------
%---------- Subscribers
%----------------------------------------

Create OrbitView DefaultOrbitView;
GMAT DefaultOrbitView.SolverIterations = Current;
GMAT DefaultOrbitView.UpperLeft = [ 0.04107142857142857 0.02380952380952381 ];
GMAT DefaultOrbitView.Size = [ 0.9886904761904762 0.9295238095238095 ];
GMAT DefaultOrbitView.RelativeZOrder = 361;
GMAT DefaultOrbitView.Maximized = false;
GMAT DefaultOrbitView.Add = {GEO1, GEO2, GEO3, Earth};
GMAT DefaultOrbitView.CoordinateSystem = EarthMJ2000Eq;
GMAT DefaultOrbitView.DrawObject = [ true true true true ];
GMAT DefaultOrbitView.DataCollectFrequency = 1;
GMAT DefaultOrbitView.UpdatePlotFrequency = 50;
GMAT DefaultOrbitView.NumPointsToRedraw = 0;
GMAT DefaultOrbitView.ShowPlot = true;
GMAT DefaultOrbitView.MaxPlotPoints = 20000;
GMAT DefaultOrbitView.ShowLabels = true;
GMAT DefaultOrbitView.ViewPointReference = Earth;
GMAT DefaultOrbitView.ViewPointVector = [ 50000 0 0 ];
GMAT DefaultOrbitView.ViewDirection = Earth;
GMAT DefaultOrbitView.ViewScaleFactor = 1;
GMAT DefaultOrbitView.ViewUpCoordinateSystem = EarthMJ2000Eq;
GMAT DefaultOrbitView.ViewUpAxis = Z;
GMAT DefaultOrbitView.EclipticPlane = Off;
GMAT DefaultOrbitView.XYPlane = On;
GMAT DefaultOrbitView.WireFrame = Off;
GMAT DefaultOrbitView.Axes = On;
GMAT DefaultOrbitView.Grid = Off;
GMAT DefaultOrbitView.SunLine = Off;
GMAT DefaultOrbitView.UseInitialView = On;
GMAT DefaultOrbitView.StarCount = 7000;
GMAT DefaultOrbitView.EnableStars = On;
GMAT DefaultOrbitView.EnableConstellations = On;

Create GroundTrackPlot DefaultGroundTrackPlot;
GMAT DefaultGroundTrackPlot.SolverIterations = Current;
GMAT DefaultGroundTrackPlot.UpperLeft = [ 0.2702380952380952 0.06571428571428571 ];
GMAT DefaultGroundTrackPlot.Size = [ 0.5107142857142857 0.9304761904761905 ];
GMAT DefaultGroundTrackPlot.RelativeZOrder = 365;
GMAT DefaultGroundTrackPlot.Maximized = false;
GMAT DefaultGroundTrackPlot.Add = {AshmoreIslands, CartierIsland, CaseyStation, ChristmasIsland, CocosIslands, CoralSeaIslands, DavisStation, GEO1, GEO2, GEO3, HeardMcDonaldIslands, MacquarieStation, MawsonStation, NorfolkIsland};
GMAT DefaultGroundTrackPlot.DataCollectFrequency = 1;
GMAT DefaultGroundTrackPlot.UpdatePlotFrequency = 50;
GMAT DefaultGroundTrackPlot.NumPointsToRedraw = 0;
GMAT DefaultGroundTrackPlot.ShowPlot = true;
GMAT DefaultGroundTrackPlot.MaxPlotPoints = 20000;
GMAT DefaultGroundTrackPlot.CentralBody = Earth;
GMAT DefaultGroundTrackPlot.TextureMap = 'ModifiedBlueMarble.jpg';

Create ReportFile ReportFile1;
GMAT ReportFile1.SolverIterations = Current;
GMAT ReportFile1.UpperLeft = [ 0 0 ];
GMAT ReportFile1.Size = [ 0 0 ];
GMAT ReportFile1.RelativeZOrder = 0;
GMAT ReportFile1.Maximized = false;
GMAT ReportFile1.Filename = 'AzElRange.txt';
GMAT ReportFile1.Precision = 16;
GMAT ReportFile1.WriteHeaders = true;
GMAT ReportFile1.LeftJustify = On;
GMAT ReportFile1.ZeroFill = Off;
GMAT ReportFile1.FixedWidth = true;
GMAT ReportFile1.Delimiter = ' ';
GMAT ReportFile1.ColumnWidth = 23;
GMAT ReportFile1.WriteReport = true;

%----------------------------------------
%---------- Functions
%----------------------------------------

Create GmatFunction CalcAzElRange;
GMAT CalcAzElRange.FunctionPath = '/Users/ninaaverill/Downloads/CalcAzElRange.gmf';

Create GmatFunction CalcAZEL;
GMAT CalcAZEL.FunctionPath = '/Users/ninaaverill/Downloads/CalcAZEL.gmf';


%----------------------------------------
%---------- Mission Sequence
%----------------------------------------

BeginMissionSequence;
While GEO1.ElapsedSecs < 86400
   Propagate DefaultProp(GEO1) DefaultProp(GEO2) DefaultProp(GEO3) {GEO1.ElapsedSecs = 300};
   GMAT 'CalcAzElForGEO1' CalcAzElRange(GEO1.EarthMJ2000Eq.X, GEO1.EarthMJ2000Eq.Y, GEO1.EarthMJ2000Eq.Z);
   GMAT 'CalcAzElForGEO2' CalcAzElRange(GEO2.EarthMJ2000Eq.X, GEO2.EarthMJ2000Eq.Y, GEO2.EarthMJ2000Eq.Z);
   GMAT 'CalcAzELForGEO3' CalcAzElRange(GEO1.EarthMJ2000Eq.X, GEO1.EarthMJ2000Eq.Y, GEO1.EarthMJ2000Eq.Z);
   Report ReportFile1 GEO1.A1ModJulian;
EndWhile;
