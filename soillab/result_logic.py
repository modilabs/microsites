# encoding=utf-8

from collections import OrderedDict


def soil_results(sample):

    def level_in_range(value, levels):
        for max_value, level in levels.iteritems():
            if not isinstance(max_value, (int, float)):
                return level
            if value < max_value:
                return level
        return levels[-1]

    # initialize results dict with labels
    n = 'name'
    v = 'value'
    b = 'badge'
    lvl = 'level_text'
    lvlt = 'level_text_verbose'
    u = 'unit'

    lvlel = u"Extremely Low"
    lvlvl = u"Very Low"
    lvll = u"Low"
    lvlm = u"Medium"
    lvlmh = u"Medium/High"
    lvlh = u"High"
    lvlvh = u"Very High"
    lvlg = u"Good"
    lvlo = u"Optimal"
    lvlb = u"No Data"

    bvl = 'important' # very low
    bvh = 'important' # very high
    bl = 'warning' # low
    bh = 'warning' # high
    bh = 'warning' # high
    bn = 'info' # neutral
    bg = 'success' # good
    bb = 'inverse' # blank
    bno = None

    udsm = u"deciS/m"
    umgc3 = u"mg/㎤"
    umgkg = u"mg/kg"
    un = None

    # initialize the result dict for ordering.
    results = OrderedDict([
        ('ec', {n: u"EC", v: 0, b: bno, lvl: lvlb, u: udsm}),
        ('ph_water', {n: u"pH Water", v: 0, b: bno, lvl: lvlb, u: un}),
        ('ph_cacl', {n: u"pH Salt", v: 0, b: bno, lvl: lvlb, u: un}),
        ('delta_ph', {n: u"Δ pH", v: 0, b: bno, lvl: lvlb, u: un}),
        ('soil_bulk_density', {n: u"Soil Bulk Density", v: 0, b: bno, lvl: lvlb, u: umgc3}),
        ('soil_moisture', {n: u"Soil Moisture at Sampling", v: 0, b: bno, lvl: lvlb, u: un}),
        ('soil_nitrate', {n: u"Soil Nitrate", v: 0, b: bno, lvl: lvlb, u: umgkg}),
        ('soil_potassium', {n: u"Soil Potassium", v: 0, b: bno, lvl: lvlb, u: umgkg}),
        ('soil_phosphorus', {n: u"Soil Phosphorus", v: 0, b: bno, lvl: lvlb, u: umgkg}),
        ('soil_sulfate', {n: u"Soil Sulfate", v: 0, b: bno, lvl: lvlb, u: umgkg}),
        # ('soil_organic_matter', {n: u"Soil Organic Matter", v: 0, b: bno, lvl: lvlb}),
    ])

    #
    # EC GROUP
    #
    soil_units = {
        'microseimens_per_cm': 1000,
        'parts_per_million': 1.0/500,
        'milliseimens_per_cm': 0.001,
        'decisiemens_per_meter': 1,
        'mmhos_per_cm': 1,
    }

    ec_levels = OrderedDict([
        (0.1, {b: bl, lvl: lvll, lvlt: u"Low fertility, leached nutrients."}),
        (0.3, {b: bn, lvl: lvlm, lvlt: u"Medium fertility, especially in acid soils."}),
        (0.6, {b: bn, lvl: lvlm, lvlt: u"Slightly saline. Limiting for salt-sensitive crops."}),
        (1.2, {b: bh, lvl: lvlh, lvlt: u"Very saline. Limiting for salt-sensitive crops. Some intolerance for salt-enduring crops."}),
        (2.4, {b: bh, lvl: lvlh, lvlt: u"Severe salinity. Strong limitations for both salt-sensitive and tolerant crops."}),
        (4.0, {b: bvh, lvl: lvlvh, lvlt: u"Very severe salinity. Few crops survive."}),
        ('_', {b: bvh, lvl: lvlvh, lvlt: u"Very few crops can grow."}),
        ])

    try:
        soil_ec = sample.get('ec_sample_ec', None) - float(sample.get('ec_blank_ec', None))
    except:
        soil_ec = None

    try:
        results['ec'][v] = soil_ec * soil_units.get(sample.get('ec_units', None), None)
    except:
        results['ec'][v] = None

    # update badge levels
    if results['ec'][v]:
        results['ec'].update(level_in_range(results['ec'][v], ec_levels))

    #
    # pH H2O
    #
    results['ph_water'][v] = sample.get('ph_water_sample_ph_water', None)

    #
    # pH CaCl
    #
    ph_cacl_levels = OrderedDict([
        (4.0, {b: bl, lvl: lvll, lvlt: u"pH is limiting: soil exhibits severe aluminum toxicity"}),
        (5.0, {b: bl, lvl: lvll, lvlt: u"pH is limiting: soil exhibits aluminum and manganese toxicity."}),
        (5.5, {b: bn, lvl: lvlm, lvlt: u"pH is somewhat limiting."}),
        (6.5, {b: bg, lvl: lvlo, lvlt: u"Optimal pH for good plant productivity."}),
        (7.5, {b: bh, lvl: lvlh, lvlt: u"pH is not limiting. However, may be Fe, Mn, Zn deficiencies in sandy soils."}),
        (8.5, {b: bh, lvl: lvlh, lvlt: u"pH is somewhat limiting (calcareous soil). Will likely observe Fe, Mn, Zn, deficiencies."}),
        ('_', {b: bvh, lvl: lvlvh, lvlt: u"Severe pH limitations with sodium problems (sodic)"}),
        ])

    results['ph_cacl'][v] = sample.get('ph_cacl2_sample_ph_cacl2', None)

     # update badge levels
    if results['ph_cacl'][v]:
        results['ph_cacl'].update(level_in_range(results['ph_cacl'][v], ph_cacl_levels))

    #
    # Δ pH
    #
    try:
        results['delta_ph'][v] = (sample.get('ph_water_sample_ph_water') 
                                  - sample.get('ph_cacl2_sample_ph_cacl2'))
    except:
        results['delta_ph'][v] = None

    #
    # soil bulk density
    #
    soil_densities = {
        'coarse': 1.6,
        'moderately_coarse': 1.4,
        'medium': 1.2,
        'fine': 1.0
    }
    results['soil_bulk_density'][v] = soil_densities.get(sample.get('sample_id_sample_soil_texture', None), None)

    #
    # soil moisture at sampling
    #
    try:
        results['soil_moisture'][v] = (sample.get('sample_id_sample_automated_soil_moisture', None) 
                                       / results['soil_bulk_density'][v])
    except:
        results['soil_moisture'][v] = None

    percent_moisture_by_weight = results['soil_moisture'][v]

    #
    # soil nitrate
    #
    nitrate_fertility_levels = OrderedDict([
        (21, {b: bvl, lvl: lvlvl, lvlt: u"Yes-Full N recommended."}),
        (42, {b: bl, lvl: lvll, lvlt: u"Yes-3/4 N recommended."}),
        (65, {b: bn, lvl: lvlm, lvlt: u"Yes-1/2 N recommended."}),
        (90, {b: bh, lvl: lvlmh, lvlt: u"Yes, 1/4 N recommended."}),
        (120, {b: bh, lvl: lvlh, lvlt: u"No N more recommended."}),
        ('_', {b: bvh, lvl: lvlvh, lvlt: u"No N recommended."}),
        ])

    try:
        results['soil_nitrate'][v] = (
            (sample.get('nitrate_sample_nitrate') 
             - sample.get('nitrate_blank_nitrate')) 
            * (30 / ((1 - percent_moisture_by_weight) * 15)) )
    except:
        results['soil_nitrate'][v] = None

     # update badge levels
    if results['soil_nitrate'][v]:
        results['soil_nitrate'].update(level_in_range(results['soil_nitrate'][v], nitrate_fertility_levels))

    #
    # soil potassium
    #
    potassium_fertility_levels = OrderedDict([
        (30, {b: bvl, lvl: lvlvl, lvlt: u"K fertilizer needed: Very Likely."}),
        (60, {b: bl, lvl: lvll, lvlt: u"K fertilizer needed: Likely."}),
        (90, {b: bn, lvl: lvlm, lvlt: u"K fertilizer needed: 50/50."}),
        (120, {b: bh, lvl: lvlh, lvlt: u"K fertilizer needed: Unlikely."}),
        ('_', {b: bvh, lvl: lvlvh, lvlt: u"No K fertilizer needed."}),
        ])

    try:
        results['soil_potassium'][v] = (
            (sample.get('potassium_sample_potassium') 
             - sample.get('potassium_blank_potassium')) 
            * (30 / ((1 - percent_moisture_by_weight) * 15)) )
    except:
        results['soil_potassium'][v] = None

     # update badge levels
    if results['soil_potassium'][v]:
        results['soil_potassium'].update(level_in_range(results['soil_potassium'][v], potassium_fertility_levels))

    #
    # soil phosphorus
    #
    phosphorus_fertility_levels = OrderedDict([
        (0.05, {b: bvl, lvl: lvlel, lvlt: u"Increasing P is top priority."}),
        (0.1, {b: bvl, lvl: lvlvl, lvlt: u"P fertilizer needed: Very Likely."}),
        (0.3, {b: bl, lvl: lvll, lvlt: u"P fertilizer needed: Likely."}),
        (0.5, {b: bn, lvl: lvlm, lvlt: u"P fertilizer needed: 50/50 chance of response."}),
        ('_', {b: bh, lvl: lvlh, lvlt: u"No P fertilizer needed."}),
        ])

    try:
        soil_phosphorus_ppb = ((sample.get('phosphorus_ppb_meter_blank_phosphorus_ppb_meter', None) 
                                - sample.get('phosphorus_ppb_meter_blank_phosphorus_ppb_meter', None))
                               * (10 / 2) 
                               * ( 30 / 
                                  ((1 - percent_moisture_by_weight) * 15)) )
    except:
        soil_phosphorus_ppb = None

    try:
        soil_phosphorus_ppm = ((sample.get('phosphorus_ppm_meter_sample_phosphorus_ppm_meter', None)
                                - sample.get('phosphorus_ppm_meter_blank_phosphorus_ppm_meter'))
                               * (10 / 2) 
                               * (30 / ((1 - percent_moisture_by_weight) * 15))
                               * (30.97 / 94.97))
    except:
        soil_phosphorus_ppm = None

    # PPB measure is preffered over PPM but might not be available.
    if soil_phosphorus_ppb is None:
        results['soil_phosphorus'][v] = soil_phosphorus_ppm
    else:
        results['soil_phosphorus'][v] = soil_phosphorus_ppb

     # update badge levels
    if results['soil_phosphorus'][v]:
        results['soil_phosphorus'].update(level_in_range(results['soil_phosphorus'][v], phosphorus_fertility_levels))

    #
    # soil sulfate
    #
    sulfate_fertility_levels = OrderedDict([
        (10, {b: bvl, lvl: lvlvl, lvlt: u"S fertilizer needed: Very Likely."}),
        (15, {b: bl, lvl: lvll, lvlt: u"S fertilizer needed: Likely."}),
        (20, {b: bn, lvl: lvlm, lvlt: u"S fertilizer needed: 50/50 chance of response."}),
        ('_', {b: bh, lvl: lvlh, lvlt: u"No S fertilizer needed."}),
        ])

    try:
        slope_low_spike_ppb = 8 / sample.get('sulfur_ppb_meter_blank_sulfur_ppb_meter', None)
    except:
        slope_low_spike_ppb = None

    try:
        slope_high_spike_ppm = 16 / sample.get('sulfur_ppm_meter_blank_sulfur_ppm_meter', None)
    except:
        slope_high_spike_ppm = None

    try:
        soil_sulfur_ppb = (((sample.get('sulfur_ppb_meter_sample_sulfur_ppb_meter', None) * slope_low_spike_ppb)
                            / sample.get('sulfur_analysis_sample_sulfur_analysis_vial_extract', None))
                           * (30 / ((1 - percent_moisture_by_weight) * 15)))
    except:
        soil_sulfur_ppb = None

    try:
        soil_sulfur_ppm = (
                            ((sample.get('sulfur_ppm_meter_sample_sulfur_ppm_meter', None) * slope_high_spike_ppm)
                              / sample.get('sulfur_analysis_sample_sulfur_analysis_vial_extract', None))
                             * (30 / ((1 - percent_moisture_by_weight) * 15)))
    except:
        soil_sulfur_ppm = None

    # PPB measure is preffered over PPM but might not be available.
    if soil_sulfur_ppb is None:
        results['soil_sulfate'][v] = soil_sulfur_ppm
    else:
        results['soil_sulfate'][v] = soil_sulfur_ppb

     # update badge levels
    if results['soil_sulfate'][v]:
        results['soil_sulfate'].update(level_in_range(results['soil_sulfate'][v], sulfate_fertility_levels))

    #
    # soil organic matter
    #
    # no input

    return results