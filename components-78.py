import gdsfactory as gf

c = gf.components.grating_coupler_elliptical_lumerical(parameters=[-2.4298362615732447, 0.1, 0.48007023217536954, 0.1, 0.607397685752365, 0.1, 0.4498844003086115, 0.1, 0.4274116312627637, 0.1, 0.4757904248387285, 0.1, 0.5026649898504233, 0.10002922416240886, 0.5100366774007897, 0.1, 0.494399635363353, 0.1079599958465788, 0.47400592737426483, 0.14972685326277918, 0.43272750134545823, 0.1839530796530385, 0.3872023336708212, 0.2360175325711591, 0.36032212454768675, 0.24261846353500535, 0.35770350120764394, 0.2606637836858316, 0.3526104381544335, 0.24668202254540886, 0.3717488388788273, 0.22920754299702897, 0.37769616507688464, 0.2246528336925301, 0.3765437598650894, 0.22041773376471022, 0.38047596041838994, 0.21923601658169187, 0.3798873698864591, 0.21700438236445285, 0.38291698672245644, 0.21827768053295463, 0.3641322152037017, 0.23729077006065105, 0.3676834419346081, 0.24865079519725933, 0.34415050295044936, 0.2733570818755685, 0.3306230780901629, 0.27350446437732157], layer='WG', layer_slab='SLAB150', taper_angle=55, taper_length=12.6, fiber_angle=5, bias_gap=0)
c.plot()