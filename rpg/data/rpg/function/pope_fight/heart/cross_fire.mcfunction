# 四束光：先是细线，一秒后才变粗开始扫。
execute positioned ^-0.03 ^1.64 ^-0.40 run function rpg:pope_fight/fx/flare
execute if score #dir rpg_pf matches 0 positioned ^-0.03 ^1.64 ^-0.40 rotated ~45 0 run function rpg:pope_fight/fx/beam_warn
execute if score #dir rpg_pf matches 0 positioned ^-0.03 ^1.64 ^-0.40 rotated ~135 0 run function rpg:pope_fight/fx/beam_warn
execute if score #dir rpg_pf matches 0 positioned ^-0.03 ^1.64 ^-0.40 rotated ~225 0 run function rpg:pope_fight/fx/beam_warn
execute if score #dir rpg_pf matches 0 positioned ^-0.03 ^1.64 ^-0.40 rotated ~315 0 run function rpg:pope_fight/fx/beam_warn
execute if score #dir rpg_pf matches 1 positioned ^-0.03 ^1.64 ^-0.40 rotated ~0 0 run function rpg:pope_fight/fx/beam_warn
execute if score #dir rpg_pf matches 1 positioned ^-0.03 ^1.64 ^-0.40 rotated ~90 0 run function rpg:pope_fight/fx/beam_warn
execute if score #dir rpg_pf matches 1 positioned ^-0.03 ^1.64 ^-0.40 rotated ~180 0 run function rpg:pope_fight/fx/beam_warn
execute if score #dir rpg_pf matches 1 positioned ^-0.03 ^1.64 ^-0.40 rotated ~270 0 run function rpg:pope_fight/fx/beam_warn
