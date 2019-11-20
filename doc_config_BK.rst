.. include:: ../references.txt

.. _analysis:

*******************************
analysis - High-level interface
*******************************

.. currentmodule:: gammapy.analysis

.. _analysis_intro:

Introduction
============

The high-level interface for Gammapy follows the recommendations written in
:ref:`pig-012`. It provides a high-level Python API for the most common use cases
identified in the analysis process. The classes and methods included may be used in
Python scripts, notebooks or as commands within IPython sessions. The high-level user
interface could also be used to automatise processes driven by parameters declared
in a configuration file in YAML format. Hence, it also provides you with different
configuration templates to address the most common analysis use cases identified.
The high-level interface allows to achieve the first analysis step that is the data
reduction and then the modeling and fitting process. The output of the data reduction
can be stored into file(s), allowing to use the datasets either with the high-level
interface or a simple notebook.

.. _analysis_start:

Getting started
===============

The easiest way to get started with the high-level interface is using it within
an IPython console or a notebook.

.. code-block:: python

    >>> from gammapy.analysis import Analysis, AnalysisConfig
    >>> config = AnalysisConfig()
    >>> analysis = Analysis(config)
        INFO:gammapy.analysis.analysis:Setting logging config: {'level': 'INFO'}

Configuration and methods
=========================

You can have a look at the configuration settings provided by default, and also dump
them into a file that you can edit to start a new analysis from the modified config file.

.. code-block:: python

    >>> print(config)
    >>> config.to_yaml("config.yaml")
    INFO:gammapy.analysis.analysis:Configuration settings saved into config.yaml
    >>> config = AnalysisConfig.from_yaml("config.yaml")

You may choose a predefined **configuration template** for your configuration. If no
value for the configuration template is provided, the ``basic`` template will be used by
default. You may dump the settings into a file, edit the file and re-initialize your
configuration from the modified file:

.. code-block:: python

    >>> config = AnalysisConfig.from_template("1d")
    >>> config.to_yaml("myconfig.yaml") # then edit the file 'myconfig.yaml'
    >>> config = AnalysisConfig.from_yaml("myconfig.yaml")

You could also have started with a built-in analysis configuration and extend it with
with your custom settings declared in a Python nested dictionary. Note how the nested
dictionary must follow the hierarchical structure of the parameters. Declaring the
configuration settings of the analysis in this way may be tedious and prone to errors
if you have several parameters to set, so we suggest you to proceed using a configuration
file:

.. code-block:: python

    >>> config = AnalysisConfig.from_template("1d")
    >>> analysis = Analysis(config)
    >>> config_dict = {"general": {"logging": {"level": "WARNING"}}}
    >>> config.update_settings(config_dict)

The hierarchical structure of the tens of parameters needed may be hard to follow. You can
print as a *how-to* documentation a helping sample config file with example values for all
the sections and parameters or only for one specific section or group of parameters:

.. code-block:: python

    >>> config.help()
    >>> config.help("flux-points")

At any moment you can change the value of one specific parameter needed in the analysis. Note
that it is a good practice to validate your settings when you modify the value of parameters:

.. code-block:: python

    >>> config.settings["reduction"]["geom"]["region"]["frame"] = "galactic"
    >>> config.validate()

It is also possible to add new configuration parameters and values or overwrite the ones already
defined in your session analysis. In this case you may use the `config.update_settings()` method
using a custom nested dictionary or custom YAML file (i.e. re-use a config file for specific
sections and/or from a previous analysis).:

.. code-block:: python

    >>> config_dict = {"observations": {"datastore": "$GAMMAPY_DATA/hess-dl3-dr1"}}
    >>> config.update_settings(config=config_dict)
    >>> config.update_settings(configfile="fit.yaml")

In the following you may find more detailed information on the different sections which
compose the YAML formatted nested configuration settings hierarchy.

General settings
----------------

The ``general`` section comprises optional information related with the ``logging`` configuration,
as well as the output folder where all file outputs and datasets will be stored, declared
as value of the ``outdir`` parameter. The default values are given here:

.. code-block:: yaml

    ## Section: general
    # General settings for the high-level interface
    general:
        # Logging settings for the session
        logging:
            # Choose one of the example values for level
            level: INFO             # Also CRITICAL, ERROR, WARNING, DEBUG
            filename: filename.log
            filemode: w             # Also 'a' for appending
            format: "%(asctime)s - %(message)s"
            datefmt: "%d-%b-%y %H:%M:%S"
        # Output folder where files will be stored
        outdir: .

Observations selection
----------------------

The observations used in the analysis may be selected using criteria defined in the ``observations`` section of the
settings. The parameters and their values of the criteria are passed to the `~gammapy.data.datastore` to build a
composed filter. The definitions of the different filters in the yaml format are the following:

.. code-block:: yaml

    ## Section: observations
    # Selection of observations used in the analysis
    observations:
        # Path where to fetch observations (from a data release)
        datastore: "$GAMMAPY_DATA/hess-dl3-dr1"

        # Selection based on a list of filters using selection criteria
        filters:
            # Filtering observations in a cone around a sky coordinate
            filter_type: sky_circle
            filter_value: frame [icrc or galactic]; lon [e.g. 83.633 deg, 83.633d]; lat [e.g. 22.014 deg, 22.014d]; cone_radius [e.g. 1 deg or 1d]
            # Filtering observations in a cone around a sky coordinate set by a source name (internet needed)
            filter_type: sky_circle
            filter_value: SourceName [e.g. 'Crab']; cone_radius  [e.g. 1 deg or 1d]
            # Filtering observations within a box of a parameter (Warning: the parameter name might depend on the data release, see the obs-index.fits file)
            filter_type: par_range
            filter_value: ParameterName [e.g. ALT_PNT, GLON_PNT, QUALITY, NSB_LEVEL]; min (e.g. 83.633 deg, 83.633d, 100.); max
            # Filtering by observation time (TO BE IMPLEMENTED! TO BE TESTED! CHECK THE FORMAT)
            filter_type: time_range
            filter_value: ['2012-01-01T01:00:00', '2012-01-01T02:00:00']; ['2012-01-01T04:00:00', '2012-01-01T05:00:00']
            # Providing a list of identifiers of the observations
            filter_type: ids
            filter_value: 23523; 23526 # As example
            # Selection of all observations
            filter_type: all

        # Observations can be excluded using some criteria, e.g.
        filters:
            filter_type: par_range
            filter_value: LIVETIME; 0. min; 15. min
            exclude: true     #This flag is used to exclude observations IDs

        # Observations can be also selected if not matching a filter, e.g.
        filters:
            filter_type: par_range
            filter_value: ALT_PNT; 0d; 20d
            inverted: true    #This flag is used to invert the selection criteria

One can combine criteria using the following syntax, respecting the `-` and the spaces alignment, e.g.:

.. code-block:: yaml
    ## Section: observations
    observations:
        filters:
            # Filtering observations in a cone around a sky coordinate
            - filter_type: sky_circle
              filter_value: 'Crab Nebula'; 2.5d

            # Filtering observations within a box of a parameter (Warning: the parameter name might depend on the data release, see the obs-index.fits file)
            - filter_type: par_range
              filter_value: LIVETIME; 0. min; 15. min
              exclude: true

The selection of observations is realised when using the `get_observations()` method. The observations are stored as a
list of `~gammapy.data.DataStoreObservation` objects.

.. code-block:: python

    >>> analysis.get_observations()
    >>> analysis.observations.list
        [<gammapy.data.observations.DataStoreObservation at 0x11e040320>,
         <gammapy.data.observations.DataStoreObservation at 0x11153d550>,
         <gammapy.data.observations.DataStoreObservation at 0x110a84160>,
         <gammapy.data.observations.DataStoreObservation at 0x110a84b38>]

Data reduction and datasets
---------------------------
The first step of the analysis is the data reduction. It consists on the reading of the DL3 data, their projection into
a format associated to the user's analysis type (e.g. 1D spectrum analysis, maps analysis, 3D analysis), and their
storage into the gammapy abstract classes called *Dataset*. Both the events and the IRFs are projected, explaining why
the data reduction step requires information for the IRFs.

The data reduction process needs a choice of a dataset type, declared as the class name
(`~gammapy.cube.MapDataset`, `~gammapy.spectrum.SpectrumDatasetOnOff`) in the ``reduction`` section of the settings.
For the estimation of the background with a dataset type `~gammapy.spectrum.SpectrumDatasetOnOff`, a
``background_estimator`` is needed. Other parameters related with the ``on_region`` and ``exclusion_mask`` FITS file
may be also present. Parameters for geometry are also needed and declared in this section, as well as a boolean flag
``stack-datasets``.

.. code-block:: yaml
    ## Section: datasets
    # Definition of the dataset type for the data reduction process
    datasets:
        dataset-type: SpectrumDatasetOnOff  # Also MapDataset
        stack-datasets: false               # If false, a list of datasets (one per obs) is stored

        # Geometry settings
        geom:
            # For the 1D spectrum extraction, definition of the ON region
            on_region: frame [icrc or galactic]; lon [e.g. 83.633 deg, 83.633d]; lat [e.g. 22.014 deg, 22.014d]; on_radius [e.g. 0.1 deg]
            containment_correction: true    # One should correct the Effective Area for the PSF leakage in this case!

            # For sky maps, set the spatial geometry
            center: frame [icrc or galactic]; lon [e.g. 83.633 deg, 83.633d]; lat [e.g. 22.014 deg, 22.014d]
            proj: CAR               # Any valid WCS projection type, e.g. AIR, HPX
            width: [5, 5]           # Width of the map in degrees
            bin_size: 0.02          # Map pixel size in degrees
            # Additional axes other than spatial to make cube
            #   Example values for reconstructed energy axis
            axes:
                - name: energy
                  axis: low_value [e.g. 0.1 TeV]; high_value [e.g. 100 TeV]; nbins [e.g. 73]   # The unit should be identical for low_value and high_value
                  interp: log       # Optional, the logarithmic interpolation is used by default ('lin' is for linear interpolation)

        # Management of the Aeff and Edisp IRFs (Optional)
        true_energy_axis:
            name: energy
            axis: low_value [e.g. 0.01 TeV]; high_value [e.g. 100 TeV]; nbins [e.g. 73]   # The unit should be identical for low_value and high_value
            interp: log       # Optional, the logarithmic interpolation is used by default ('lin' is for linear interpolation)
        bin_size_irf: 0.02    # IRF map pixel size in degrees
        margin_irf: 0.05      # IRF map margin size in degrees

        # Parameters for the estimation of the background when using SpectrumDatasetOnOff
        background:
            background_estimator: reflected
            exclusion_mask:
                filename: mask.fits
                hdu: IMAGE

The method `make_datasets()` allows you to proceed to the data reduction process.
The final reduced datasets are stored in the ``datasets`` attribute.
For spectral reduction the information related with the background estimation is
stored in the ``background_estimator`` property.

.. code-block:: python

    >>> analysis.make_datasets()
    >>> analysis.datasets.datasets
        [SpectrumDatasetOnOff,
         SpectrumDatasetOnOff,
         SpectrumDatasetOnOff,
         SpectrumDatasetOnOff,
         SpectrumDatasetOnOff,
         SpectrumDatasetOnOff,
         SpectrumDatasetOnOff,
         SpectrumDatasetOnOff]
    >>> analysis.background_estimator.on_region
        <CircleSkyRegion(<SkyCoord (ICRS): (ra, dec) in deg
            (83.633, 22.014)>, radius=0.1 deg)>

The datasets can be stored into disk by using the method `~gammapy.modeling.datasets.to_yaml',
and read back with `~gammapy.modeling.datasets.from_yaml'.


Model
-----

After the data reduction steps, one can go for the modeling and the fitting of the datasets.
The model can be declare in the previous YAML file in the ``model'' section. Or we can simply
declare the model as a reference to a separate YAML file, passing the filename into the
`set_model()` method to fetch the model and attach it to your datasets. Note that you may also
pass a serialized model as a dictionary.

.. code-block:: yaml
    ## Section: model
    # Definition of the source model for the next step of fitting
    model:
        components:
        - name: crab
          type: SkyModel
          spatial:
            type: PointSpatialModel
            frame: [icrc or galactic]
            parameters:
            - name: lon_0
              value: 83.63
              unit: deg
              frozen: false # Optional
            - name: lat_0
              value: 22.14
              unit: deg
              frozen: false # Optional
          spectral:
            type: PowerLawSpectralModel
            parameters:
            - name: amplitude
              value: 1.0e-12
              unit: cm-2 s-1 TeV-1
            - name: index
              value: 2.0
              unit: ''
            - name: reference
              value: 1.0
              unit: TeV
          frozen: true  # Optional

.. code-block:: python

    >>> analysis.set_model(filename="model.yaml")   # If stored into a separate file
    >>> analysis.set_model(model=dict_model)        # If stored into a dictionary

Fitting
-------

The parameters used in the fitting process are declared in the ``fit`` section.

.. code-block:: yaml

    ## Section: fit
    # Fitting process
    fit:
        fit_range:
            min: 1 TeV
            max: 100 TeV
        # Later the energy threshold strategy

You may use the `run_fit()` method to proceed to the model fitting process. The result
is stored in the ``fit_result`` property.

.. code-block:: python

    >>> analysis.run_fit()
    >>> analysis.fit_result
        OptimizeResult

            backend    : minuit
            method     : minuit
            success    : True
            message    : Optimization terminated successfully.
            nfev       : 111
            total stat : 239.28

Flux points
-----------

For spectral analysis where we aim to calculate flux points in a range of energies, we
may declare the parameters needed in the ``flux-points`` section.

.. code-block:: yaml

    ## Section: flux-points
    # Flux estimation process
    flux-points:
        fp_binning:
            axis: low_value [e.g. 1 TeV]; high_value [e.g. 10 TeV]; nbins [e.g. 10]   # The unit should be identical for low_value and high_value
            interp: log         # Optional, the logarithmic interpolation is used by default ('lin' is for linear interpolation)
            node_type: edges    # By default, Optional

You may use the `get_flux_points()` method to calculate the flux points. The result
is stored in the ``flux_points`` property as a `~gammapy.spectrum.FluxPoints` object.

.. code-block:: python

    >>> analysis.get_flux_points()
        INFO:gammapy.analysis.analysis:Calculating flux points.
        INFO:gammapy.analysis.analysis:
              e_ref               ref_flux                 dnde                 dnde_ul                dnde_err        is_ul
               TeV              1 / (cm2 s)          1 / (cm2 s TeV)        1 / (cm2 s TeV)        1 / (cm2 s TeV)
        ------------------ ---------------------- ---------------------- ---------------------- ---------------------- -----
        1.1364636663857248   5.82540193791155e-12 1.6945571729283257e-11 2.0092001005968464e-11  1.491004091925887e-12 False
        1.3768571648527583 2.0986802770569557e-12 1.1137098968561381e-11 1.4371773951168255e-11  1.483696107656724e-12 False
        1.6681005372000581 3.0592927032553813e-12  8.330762241576842e-12   9.97704078861513e-12  7.761855010963746e-13 False
        2.1544346900318834  1.991366151205521e-12  3.749504881244244e-12  4.655825384923802e-12  4.218641798406146e-13 False
        2.6101572156825363  7.174167397335237e-13 2.3532638339895766e-12 3.2547227459669707e-12   4.05804720903438e-13 False
        3.1622776601683777 1.0457942646403696e-12 1.5707172671966065e-12 2.0110274930777325e-12 2.0291499028818014e-13 False
         3.831186849557287 3.7676160725948056e-13  6.988070884720634e-13 1.0900735920193252e-12 1.6898704308171627e-13 False
        4.6415888336127775  5.492137361542478e-13 4.2471136559991427e-13  6.095655421226728e-13  8.225678668637978e-14 False
         5.994842503189405 3.5749624179174077e-13 2.2261366353081893e-13  3.350617464903039e-13  4.898878805758816e-14 False
          7.26291750173621 1.2879288326657447e-13 2.5317668601400673e-13 4.0803852787540073e-13  6.601201499048379e-14 False
          8.79922543569107  1.877442373267013e-13  7.097738087032472e-14  1.254638299336029e-13 2.2705519890120373e-14 False
    >>> analysis.flux_points.peek()

Residuals
---------

For 3D analysis we can compute a residual image to check how good are the models
for the source and/or the background.

.. code-block:: python

    >>> analysis.datasets.datasets[0].residuals()
            geom  : WcsGeom
            axes  : ['lon', 'lat', 'energy']
            shape : (250, 250, 4)
            ndim  : 3
            unit  :
            dtype : float64

Using the high-level interface
------------------------------

Gammapy tutorial notebooks that show examples using the high-level interface:

* `First analysis <../notebooks/analysis_1.html>`__

Reference/API
=============

.. automodapi:: gammapy.analysis
    :no-inheritance-diagram:
    :include-all-objects: