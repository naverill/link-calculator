%General Mission Analysis Tool(GMAT) Script
%Created: 2022-04-07 12:29:17


%----------------------------------------
%---------- Spacecraft
%----------------------------------------

Create Spacecraft COMMSAT1;
GMAT COMMSAT1.DateFormat = TAIModJulian;
GMAT COMMSAT1.Epoch = '21545';
GMAT COMMSAT1.CoordinateSystem = EarthMJ2000Eq;
GMAT COMMSAT1.DisplayStateType = Keplerian;
GMAT COMMSAT1.SMA = 42164.99999999999;
GMAT COMMSAT1.ECC = 3.794636528864267e-16;
GMAT COMMSAT1.INC = 29.99999999999998;
GMAT COMMSAT1.RAAN = 30;
GMAT COMMSAT1.AOP = 0;
GMAT COMMSAT1.TA = 1.207418269725733e-06;
GMAT COMMSAT1.DryMass = 850;
GMAT COMMSAT1.Cd = 2.2;
GMAT COMMSAT1.Cr = 1.8;
GMAT COMMSAT1.DragArea = 15;
GMAT COMMSAT1.SRPArea = 1;
GMAT COMMSAT1.SPADDragScaleFactor = 1;
GMAT COMMSAT1.SPADSRPScaleFactor = 1;
GMAT COMMSAT1.NAIFId = -10001001;
GMAT COMMSAT1.NAIFIdReferenceFrame = -9001001;
GMAT COMMSAT1.OrbitColor = Red;
GMAT COMMSAT1.TargetColor = Teal;
GMAT COMMSAT1.OrbitErrorCovariance = [ 1e+70 0 0 0 0 0 ; 0 1e+70 0 0 0 0 ; 0 0 1e+70 0 0 0 ; 0 0 0 1e+70 0 0 ; 0 0 0 0 1e+70 0 ; 0 0 0 0 0 1e+70 ];
GMAT COMMSAT1.CdSigma = 1e+70;
GMAT COMMSAT1.CrSigma = 1e+70;
GMAT COMMSAT1.Id = 'SatId';
GMAT COMMSAT1.Attitude = CoordinateSystemFixed;
GMAT COMMSAT1.SPADSRPInterpolationMethod = Bilinear;
GMAT COMMSAT1.SPADSRPScaleFactorSigma = 1e+70;
GMAT COMMSAT1.SPADDragInterpolationMethod = Bilinear;
GMAT COMMSAT1.SPADDragScaleFactorSigma = 1e+70;
GMAT COMMSAT1.ModelFile = 'aura.3ds';
GMAT COMMSAT1.ModelOffsetX = 0;
GMAT COMMSAT1.ModelOffsetY = 0;
GMAT COMMSAT1.ModelOffsetZ = 0;
GMAT COMMSAT1.ModelRotationX = 0;
GMAT COMMSAT1.ModelRotationY = 0;
GMAT COMMSAT1.ModelRotationZ = 0;
GMAT COMMSAT1.ModelScale = 1;
GMAT COMMSAT1.AttitudeDisplayStateType = 'Quaternion';
GMAT COMMSAT1.AttitudeRateDisplayStateType = 'AngularVelocity';
GMAT COMMSAT1.AttitudeCoordinateSystem = EarthMJ2000Eq;
GMAT COMMSAT1.EulerAngleSequence = '321';

%----------------------------------------
%---------- Spacecraft
%----------------------------------------

Create Spacecraft COMMSAT2;
GMAT COMMSAT2.DateFormat = TAIModJulian;
GMAT COMMSAT2.Epoch = '21545';
GMAT COMMSAT2.CoordinateSystem = EarthMJ2000Eq;
GMAT COMMSAT2.DisplayStateType = Keplerian;
GMAT COMMSAT2.SMA = 42164.99999999999;
GMAT COMMSAT2.ECC = 1.192684599010012e-15;
GMAT COMMSAT2.INC = 30;
GMAT COMMSAT2.RAAN = 150;
GMAT COMMSAT2.AOP = 0;
GMAT COMMSAT2.TA = 239.9999999999998;
GMAT COMMSAT2.DryMass = 850;
GMAT COMMSAT2.Cd = 2.2;
GMAT COMMSAT2.Cr = 1.8;
GMAT COMMSAT2.DragArea = 15;
GMAT COMMSAT2.SRPArea = 1;
GMAT COMMSAT2.SPADDragScaleFactor = 1;
GMAT COMMSAT2.SPADSRPScaleFactor = 1;
GMAT COMMSAT2.NAIFId = -10001001;
GMAT COMMSAT2.NAIFIdReferenceFrame = -9001001;
GMAT COMMSAT2.OrbitColor = Red;
GMAT COMMSAT2.TargetColor = Teal;
GMAT COMMSAT2.OrbitErrorCovariance = [ 1e+70 0 0 0 0 0 ; 0 1e+70 0 0 0 0 ; 0 0 1e+70 0 0 0 ; 0 0 0 1e+70 0 0 ; 0 0 0 0 1e+70 0 ; 0 0 0 0 0 1e+70 ];
GMAT COMMSAT2.CdSigma = 1e+70;
GMAT COMMSAT2.CrSigma = 1e+70;
GMAT COMMSAT2.Id = 'SatId';
GMAT COMMSAT2.Attitude = CoordinateSystemFixed;
GMAT COMMSAT2.SPADSRPInterpolationMethod = Bilinear;
GMAT COMMSAT2.SPADSRPScaleFactorSigma = 1e+70;
GMAT COMMSAT2.SPADDragInterpolationMethod = Bilinear;
GMAT COMMSAT2.SPADDragScaleFactorSigma = 1e+70;
GMAT COMMSAT2.ModelFile = 'aura.3ds';
GMAT COMMSAT2.ModelOffsetX = 0;
GMAT COMMSAT2.ModelOffsetY = 0;
GMAT COMMSAT2.ModelOffsetZ = 0;
GMAT COMMSAT2.ModelRotationX = 0;
GMAT COMMSAT2.ModelRotationY = 0;
GMAT COMMSAT2.ModelRotationZ = 0;
GMAT COMMSAT2.ModelScale = 1;
GMAT COMMSAT2.AttitudeDisplayStateType = 'Quaternion';
GMAT COMMSAT2.AttitudeRateDisplayStateType = 'AngularVelocity';
GMAT COMMSAT2.AttitudeCoordinateSystem = EarthMJ2000Eq;
GMAT COMMSAT2.EulerAngleSequence = '321';

%----------------------------------------
%---------- Spacecraft
%----------------------------------------

Create Spacecraft COMMSAT3;
GMAT COMMSAT3.DateFormat = TAIModJulian;
GMAT COMMSAT3.Epoch = '21545';
GMAT COMMSAT3.CoordinateSystem = EarthMJ2000Eq;
GMAT COMMSAT3.DisplayStateType = Keplerian;
GMAT COMMSAT3.SMA = 42164.99999999999;
GMAT COMMSAT3.ECC = 1.293181873398937e-15;
GMAT COMMSAT3.INC = 29.99999999999997;
GMAT COMMSAT3.RAAN = 270;
GMAT COMMSAT3.AOP = 0;
GMAT COMMSAT3.TA = 120;
GMAT COMMSAT3.DryMass = 850;
GMAT COMMSAT3.Cd = 2.2;
GMAT COMMSAT3.Cr = 1.8;
GMAT COMMSAT3.DragArea = 15;
GMAT COMMSAT3.SRPArea = 1;
GMAT COMMSAT3.SPADDragScaleFactor = 1;
GMAT COMMSAT3.SPADSRPScaleFactor = 1;
GMAT COMMSAT3.NAIFId = -10001001;
GMAT COMMSAT3.NAIFIdReferenceFrame = -9001001;
GMAT COMMSAT3.OrbitColor = Red;
GMAT COMMSAT3.TargetColor = Teal;
GMAT COMMSAT3.OrbitErrorCovariance = [ 1e+70 0 0 0 0 0 ; 0 1e+70 0 0 0 0 ; 0 0 1e+70 0 0 0 ; 0 0 0 1e+70 0 0 ; 0 0 0 0 1e+70 0 ; 0 0 0 0 0 1e+70 ];
GMAT COMMSAT3.CdSigma = 1e+70;
GMAT COMMSAT3.CrSigma = 1e+70;
GMAT COMMSAT3.Id = 'SatId';
GMAT COMMSAT3.Attitude = CoordinateSystemFixed;
GMAT COMMSAT3.SPADSRPInterpolationMethod = Bilinear;
GMAT COMMSAT3.SPADSRPScaleFactorSigma = 1e+70;
GMAT COMMSAT3.SPADDragInterpolationMethod = Bilinear;
GMAT COMMSAT3.SPADDragScaleFactorSigma = 1e+70;
GMAT COMMSAT3.ModelFile = 'aura.3ds';
GMAT COMMSAT3.ModelOffsetX = 0;
GMAT COMMSAT3.ModelOffsetY = 0;
GMAT COMMSAT3.ModelOffsetZ = 0;
GMAT COMMSAT3.ModelRotationX = 0;
GMAT COMMSAT3.ModelRotationY = 0;
GMAT COMMSAT3.ModelRotationZ = 0;
GMAT COMMSAT3.ModelScale = 1;
GMAT COMMSAT3.AttitudeDisplayStateType = 'Quaternion';
GMAT COMMSAT3.AttitudeRateDisplayStateType = 'AngularVelocity';
GMAT COMMSAT3.AttitudeCoordinateSystem = EarthMJ2000Eq;
GMAT COMMSAT3.EulerAngleSequence = '321';

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
GMAT ContactLocator1.Target = COMMSAT1;
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
GMAT ContactLocator2.Target = COMMSAT2;
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
GMAT ContactLocator3.Target = COMMSAT3;
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

Create EclipseLocator EclipseLocator1;
GMAT EclipseLocator1.Spacecraft = COMMSAT3;
GMAT EclipseLocator1.Filename = 'EclipseLocator1.txt';
GMAT EclipseLocator1.OccultingBodies = {Earth, Luna};
GMAT EclipseLocator1.InputEpochFormat = 'TAIModJulian';
GMAT EclipseLocator1.InitialEpoch = '21545';
GMAT EclipseLocator1.StepSize = 10;
GMAT EclipseLocator1.FinalEpoch = '21545.138';
GMAT EclipseLocator1.UseLightTimeDelay = true;
GMAT EclipseLocator1.UseStellarAberration = true;
GMAT EclipseLocator1.WriteReport = true;
GMAT EclipseLocator1.RunMode = Automatic;
GMAT EclipseLocator1.UseEntireInterval = true;
GMAT EclipseLocator1.EclipseTypes = {'Umbra', 'Penumbra', 'Antumbra'};

Create EclipseLocator EclipseLocator2;
GMAT EclipseLocator2.Spacecraft = COMMSAT2;
GMAT EclipseLocator2.Filename = 'EclipseLocator1.txt';
GMAT EclipseLocator2.OccultingBodies = {Earth, Luna};
GMAT EclipseLocator2.InputEpochFormat = 'TAIModJulian';
GMAT EclipseLocator2.InitialEpoch = '21545';
GMAT EclipseLocator2.StepSize = 10;
GMAT EclipseLocator2.FinalEpoch = '21545.138';
GMAT EclipseLocator2.UseLightTimeDelay = true;
GMAT EclipseLocator2.UseStellarAberration = true;
GMAT EclipseLocator2.WriteReport = true;
GMAT EclipseLocator2.RunMode = Automatic;
GMAT EclipseLocator2.UseEntireInterval = true;
GMAT EclipseLocator2.EclipseTypes = {'Umbra', 'Penumbra', 'Antumbra'};

Create EclipseLocator EclipseLocator3;
GMAT EclipseLocator3.Spacecraft = COMMSAT2;
GMAT EclipseLocator3.Filename = 'EclipseLocator1.txt';
GMAT EclipseLocator3.OccultingBodies = {Earth, Luna};
GMAT EclipseLocator3.InputEpochFormat = 'TAIModJulian';
GMAT EclipseLocator3.InitialEpoch = '21545';
GMAT EclipseLocator3.StepSize = 10;
GMAT EclipseLocator3.FinalEpoch = '21545.138';
GMAT EclipseLocator3.UseLightTimeDelay = true;
GMAT EclipseLocator3.UseStellarAberration = true;
GMAT EclipseLocator3.WriteReport = true;
GMAT EclipseLocator3.RunMode = Automatic;
GMAT EclipseLocator3.UseEntireInterval = true;
GMAT EclipseLocator3.EclipseTypes = {'Umbra', 'Penumbra', 'Antumbra'};

%----------------------------------------
%---------- Subscribers
%----------------------------------------

Create OrbitView EarthFixedEcliptic;
GMAT EarthFixedEcliptic.SolverIterations = None;
GMAT EarthFixedEcliptic.UpperLeft = [ 0.09761904761904762 0.08190476190476191 ];
GMAT EarthFixedEcliptic.Size = [ 0.6976190476190476 0.7342857142857143 ];
GMAT EarthFixedEcliptic.RelativeZOrder = 388;
GMAT EarthFixedEcliptic.Maximized = false;
GMAT EarthFixedEcliptic.Add = {COMMSAT1, COMMSAT2, COMMSAT3, Earth};
GMAT EarthFixedEcliptic.CoordinateSystem = EarthFixed;
GMAT EarthFixedEcliptic.DrawObject = [ true true true true ];
GMAT EarthFixedEcliptic.DataCollectFrequency = 1;
GMAT EarthFixedEcliptic.UpdatePlotFrequency = 50;
GMAT EarthFixedEcliptic.NumPointsToRedraw = 0;
GMAT EarthFixedEcliptic.ShowPlot = true;
GMAT EarthFixedEcliptic.MaxPlotPoints = 20000;
GMAT EarthFixedEcliptic.ShowLabels = true;
GMAT EarthFixedEcliptic.ViewPointReference = Earth;
GMAT EarthFixedEcliptic.ViewPointVector = COMMSAT1;
GMAT EarthFixedEcliptic.ViewDirection = Earth;
GMAT EarthFixedEcliptic.ViewScaleFactor = 2.5;
GMAT EarthFixedEcliptic.ViewUpCoordinateSystem = EarthMJ2000Eq;
GMAT EarthFixedEcliptic.ViewUpAxis = Z;
GMAT EarthFixedEcliptic.EclipticPlane = On;
GMAT EarthFixedEcliptic.XYPlane = Off;
GMAT EarthFixedEcliptic.WireFrame = Off;
GMAT EarthFixedEcliptic.Axes = On;
GMAT EarthFixedEcliptic.Grid = Off;
GMAT EarthFixedEcliptic.SunLine = Off;
GMAT EarthFixedEcliptic.UseInitialView = On;
GMAT EarthFixedEcliptic.StarCount = 7000;
GMAT EarthFixedEcliptic.EnableStars = On;
GMAT EarthFixedEcliptic.EnableConstellations = On;

Create GroundTrackPlot DefaultGroundTrackPlot;
GMAT DefaultGroundTrackPlot.SolverIterations = Current;
GMAT DefaultGroundTrackPlot.UpperLeft = [ 0.05773809523809524 0.03142857142857143 ];
GMAT DefaultGroundTrackPlot.Size = [ 0.9898809523809524 0.9533333333333334 ];
GMAT DefaultGroundTrackPlot.RelativeZOrder = 408;
GMAT DefaultGroundTrackPlot.Maximized = false;
GMAT DefaultGroundTrackPlot.Add = {AshmoreIslands, CartierIsland, CaseyStation, ChristmasIsland, CocosIslands, CoralSeaIslands, DavisStation, COMMSAT1, COMMSAT2, COMMSAT3, HeardMcDonaldIslands, MacquarieStation, MawsonStation, NorfolkIsland};
GMAT DefaultGroundTrackPlot.DataCollectFrequency = 1;
GMAT DefaultGroundTrackPlot.UpdatePlotFrequency = 50;
GMAT DefaultGroundTrackPlot.NumPointsToRedraw = 0;
GMAT DefaultGroundTrackPlot.ShowPlot = true;
GMAT DefaultGroundTrackPlot.MaxPlotPoints = 20000;
GMAT DefaultGroundTrackPlot.CentralBody = Earth;
GMAT DefaultGroundTrackPlot.TextureMap = 'ModifiedBlueMarble.jpg';

Create ReportFile ReportFile1;
GMAT ReportFile1.SolverIterations = Current;
GMAT ReportFile1.UpperLeft = [ 0.1458333333333333 0.03656998738965952 ];
GMAT ReportFile1.Size = [ 0.9940476190476191 0.9609079445145019 ];
GMAT ReportFile1.RelativeZOrder = 121;
GMAT ReportFile1.Maximized = true;
GMAT ReportFile1.Filename = 'OrbitParams.txt';
GMAT ReportFile1.Precision = 16;
GMAT ReportFile1.Add = {COMMSAT1.UTCGregorian, COMMSAT1.Earth.TA, COMMSAT1.Earth.Latitude, COMMSAT1.Earth.Longitude, COMMSAT1.Earth.RMAG, COMMSAT1.Earth.Altitude, COMMSAT2.Earth.TA, COMMSAT2.Earth.Latitude, COMMSAT2.Earth.Longitude, COMMSAT2.Earth.RMAG, COMMSAT3.Earth.TA, COMMSAT3.Earth.Latitude, COMMSAT3.Earth.Longitude, COMMSAT3.Earth.RMAG};
GMAT ReportFile1.WriteHeaders = true;
GMAT ReportFile1.LeftJustify = On;
GMAT ReportFile1.ZeroFill = Off;
GMAT ReportFile1.FixedWidth = true;
GMAT ReportFile1.Delimiter = ' ';
GMAT ReportFile1.ColumnWidth = 23;
GMAT ReportFile1.WriteReport = true;

Create OrbitView J2000Ecliptic;
GMAT J2000Ecliptic.SolverIterations = None;
GMAT J2000Ecliptic.UpperLeft = [ 0.1035714285714286 0.04571428571428571 ];
GMAT J2000Ecliptic.Size = [ 0.8101190476190476 0.8504761904761905 ];
GMAT J2000Ecliptic.RelativeZOrder = 406;
GMAT J2000Ecliptic.Maximized = false;
GMAT J2000Ecliptic.Add = {COMMSAT1, COMMSAT2, COMMSAT3, Earth};
GMAT J2000Ecliptic.CoordinateSystem = EarthMJ2000Eq;
GMAT J2000Ecliptic.DrawObject = [ true true true true ];
GMAT J2000Ecliptic.DataCollectFrequency = 1;
GMAT J2000Ecliptic.UpdatePlotFrequency = 50;
GMAT J2000Ecliptic.NumPointsToRedraw = 0;
GMAT J2000Ecliptic.ShowPlot = true;
GMAT J2000Ecliptic.MaxPlotPoints = 20000;
GMAT J2000Ecliptic.ShowLabels = true;
GMAT J2000Ecliptic.ViewPointReference = Earth;
GMAT J2000Ecliptic.ViewPointVector = COMMSAT1;
GMAT J2000Ecliptic.ViewDirection = Earth;
GMAT J2000Ecliptic.ViewScaleFactor = 2.5;
GMAT J2000Ecliptic.ViewUpCoordinateSystem = EarthMJ2000Eq;
GMAT J2000Ecliptic.ViewUpAxis = Z;
GMAT J2000Ecliptic.EclipticPlane = On;
GMAT J2000Ecliptic.XYPlane = Off;
GMAT J2000Ecliptic.WireFrame = Off;
GMAT J2000Ecliptic.Axes = On;
GMAT J2000Ecliptic.Grid = Off;
GMAT J2000Ecliptic.SunLine = Off;
GMAT J2000Ecliptic.UseInitialView = On;
GMAT J2000Ecliptic.StarCount = 7000;
GMAT J2000Ecliptic.EnableStars = On;
GMAT J2000Ecliptic.EnableConstellations = On;

%----------------------------------------
%---------- Subscribers
%----------------------------------------

Create OrbitView EarthFixedXY;
GMAT EarthFixedXY.SolverIterations = None;
GMAT EarthFixedXY.UpperLeft = [ 0.09345238095238095 0.03619047619047619 ];
GMAT EarthFixedXY.Size = [ 0.7738095238095238 0.820952380952381 ];
GMAT EarthFixedXY.RelativeZOrder = 400;
GMAT EarthFixedXY.Maximized = false;
GMAT EarthFixedXY.Add = {COMMSAT1, COMMSAT2, COMMSAT3, Earth};
GMAT EarthFixedXY.CoordinateSystem = EarthFixed;
GMAT EarthFixedXY.DrawObject = [ true true true true ];
GMAT EarthFixedXY.DataCollectFrequency = 1;
GMAT EarthFixedXY.UpdatePlotFrequency = 50;
GMAT EarthFixedXY.NumPointsToRedraw = 0;
GMAT EarthFixedXY.ShowPlot = true;
GMAT EarthFixedXY.MaxPlotPoints = 20000;
GMAT EarthFixedXY.ShowLabels = true;
GMAT EarthFixedXY.ViewPointReference = Earth;
GMAT EarthFixedXY.ViewPointVector = COMMSAT1;
GMAT EarthFixedXY.ViewDirection = Earth;
GMAT EarthFixedXY.ViewScaleFactor = 2.5;
GMAT EarthFixedXY.ViewUpCoordinateSystem = EarthMJ2000Eq;
GMAT EarthFixedXY.ViewUpAxis = Z;
GMAT EarthFixedXY.EclipticPlane = Off;
GMAT EarthFixedXY.XYPlane = On;
GMAT EarthFixedXY.WireFrame = Off;
GMAT EarthFixedXY.Axes = On;
GMAT EarthFixedXY.Grid = Off;
GMAT EarthFixedXY.SunLine = Off;
GMAT EarthFixedXY.UseInitialView = On;
GMAT EarthFixedXY.StarCount = 7000;
GMAT EarthFixedXY.EnableStars = On;
GMAT EarthFixedXY.EnableConstellations = On;

Create OrbitView J2000XY;
GMAT J2000XY.SolverIterations = None;
GMAT J2000XY.UpperLeft = [ 0.1571428571428571 0.08476190476190476 ];
GMAT J2000XY.Size = [ 0.7053571428571429 0.7495238095238095 ];
GMAT J2000XY.RelativeZOrder = 394;
GMAT J2000XY.Maximized = false;
GMAT J2000XY.Add = {COMMSAT1, COMMSAT2, COMMSAT3, Earth};
GMAT J2000XY.CoordinateSystem = EarthMJ2000Eq;
GMAT J2000XY.DrawObject = [ true true true true ];
GMAT J2000XY.DataCollectFrequency = 1;
GMAT J2000XY.UpdatePlotFrequency = 50;
GMAT J2000XY.NumPointsToRedraw = 0;
GMAT J2000XY.ShowPlot = true;
GMAT J2000XY.MaxPlotPoints = 20000;
GMAT J2000XY.ShowLabels = true;
GMAT J2000XY.ViewPointReference = Earth;
GMAT J2000XY.ViewPointVector = COMMSAT1;
GMAT J2000XY.ViewDirection = Earth;
GMAT J2000XY.ViewScaleFactor = 2.5;
GMAT J2000XY.ViewUpCoordinateSystem = EarthMJ2000Eq;
GMAT J2000XY.ViewUpAxis = Z;
GMAT J2000XY.EclipticPlane = Off;
GMAT J2000XY.XYPlane = On;
GMAT J2000XY.WireFrame = Off;
GMAT J2000XY.Axes = On;
GMAT J2000XY.Grid = Off;
GMAT J2000XY.SunLine = Off;
GMAT J2000XY.UseInitialView = On;
GMAT J2000XY.StarCount = 7000;
GMAT J2000XY.EnableStars = On;
GMAT J2000XY.EnableConstellations = On;

%----------------------------------------
%---------- Functions
%----------------------------------------

Create GmatFunction CalcAzElRange;
GMAT CalcAzElRange.FunctionPath = '/Users/ninaaverill/unispace/2022/zeit8219-Satellite-Communications/assmt1/CalcAzElRange.gmf';

%----------------------------------------
%---------- Arrays, Variables, Strings
%----------------------------------------
Create Variable EarthRad;
GMAT EarthRad = 6371;



%----------------------------------------
%---------- Mission Sequence
%----------------------------------------

BeginMissionSequence;
While COMMSAT1.ElapsedSecs < 86400
   Propagate DefaultProp(COMMSAT1) DefaultProp(COMMSAT2) DefaultProp(COMMSAT3) {COMMSAT1.ElapsedSecs = 300};
   Report ReportFile1 COMMSAT1.UTCGregorian COMMSAT1.Earth.TA COMMSAT1.Earth.Latitude COMMSAT1.Earth.Longitude COMMSAT1.Earth.RMAG COMMSAT1.Earth.Altitude COMMSAT2.Earth.TA COMMSAT2.Earth.Latitude COMMSAT2.Earth.Longitude COMMSAT2.Earth.RMAG COMMSAT3.Earth.TA COMMSAT3.Earth.Latitude COMMSAT3.Earth.Longitude COMMSAT3.Earth.RMAG;
EndWhile;
