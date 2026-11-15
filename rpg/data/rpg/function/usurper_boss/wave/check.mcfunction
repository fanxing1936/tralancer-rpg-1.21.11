# 召役血线（as/at 载体，空闲时）
execute if score @s rpg_ub_h matches ..1000 unless entity @s[tag=rpg.usb.w0] run return run function rpg:usurper_boss/wave/at0
execute if score @s rpg_ub_h matches ..750 unless entity @s[tag=rpg.usb.w1] run return run function rpg:usurper_boss/wave/at1
execute if score @s rpg_ub_h matches ..500 unless entity @s[tag=rpg.usb.w2] run return run function rpg:usurper_boss/wave/at2
execute if score @s rpg_ub_h matches ..250 unless entity @s[tag=rpg.usb.w3] run return run function rpg:usurper_boss/wave/at3
