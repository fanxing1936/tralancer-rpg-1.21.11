execute store result storage rpg:explore k.pt int 1 run scoreboard players get @s rpg_x_pt
execute store result storage rpg:explore k.bn int 1 run scoreboard players get @s rpg_xb_n
execute store result storage rpg:explore k.tn int 1 run scoreboard players get @s rpg_xt_n
execute store result storage rpg:explore k.zombie int 1 run scoreboard players get @s rpg_kl_zombie
execute store result storage rpg:explore k.husk int 1 run scoreboard players get @s rpg_kl_husk
execute store result storage rpg:explore k.drowned int 1 run scoreboard players get @s rpg_kl_drowned
execute store result storage rpg:explore k.skeleton int 1 run scoreboard players get @s rpg_kl_skeleton
execute store result storage rpg:explore k.stray int 1 run scoreboard players get @s rpg_kl_stray
execute store result storage rpg:explore k.bogged int 1 run scoreboard players get @s rpg_kl_bogged
execute store result storage rpg:explore k.spider int 1 run scoreboard players get @s rpg_kl_spider
execute store result storage rpg:explore k.cave_spider int 1 run scoreboard players get @s rpg_kl_cave_spider
execute store result storage rpg:explore k.creeper int 1 run scoreboard players get @s rpg_kl_creeper
execute store result storage rpg:explore k.enderman int 1 run scoreboard players get @s rpg_kl_enderman
execute store result storage rpg:explore k.witch int 1 run scoreboard players get @s rpg_kl_witch
execute store result storage rpg:explore k.pillager int 1 run scoreboard players get @s rpg_kl_pillager
execute store result storage rpg:explore k.vindicator int 1 run scoreboard players get @s rpg_kl_vindicator
execute store result storage rpg:explore k.evoker int 1 run scoreboard players get @s rpg_kl_evoker
execute store result storage rpg:explore k.ravager int 1 run scoreboard players get @s rpg_kl_ravager
execute store result storage rpg:explore k.phantom int 1 run scoreboard players get @s rpg_kl_phantom
execute store result storage rpg:explore k.slime int 1 run scoreboard players get @s rpg_kl_slime
execute store result storage rpg:explore k.silverfish int 1 run scoreboard players get @s rpg_kl_silverfish
execute store result storage rpg:explore k.blaze int 1 run scoreboard players get @s rpg_kl_blaze
execute store result storage rpg:explore k.wither_skeleton int 1 run scoreboard players get @s rpg_kl_wither_skeleton
execute store result storage rpg:explore k.magma_cube int 1 run scoreboard players get @s rpg_kl_magma_cube
execute store result storage rpg:explore k.ghast int 1 run scoreboard players get @s rpg_kl_ghast
execute store result storage rpg:explore k.piglin_brute int 1 run scoreboard players get @s rpg_kl_piglin_brute
execute store result storage rpg:explore k.hoglin int 1 run scoreboard players get @s rpg_kl_hoglin
execute store result storage rpg:explore k.guardian int 1 run scoreboard players get @s rpg_kl_guardian
execute store result storage rpg:explore k.breeze int 1 run scoreboard players get @s rpg_kl_breeze
execute store result storage rpg:explore k.ms_sword int 1 run scoreboard players get @s rpg_ms_sword
execute store result storage rpg:explore k.ms_axe int 1 run scoreboard players get @s rpg_ms_axe
execute store result storage rpg:explore k.ms_mace int 1 run scoreboard players get @s rpg_ms_mace
execute store result storage rpg:explore k.ms_bow int 1 run scoreboard players get @s rpg_ms_bow
execute store result storage rpg:explore k.ms_crossbow int 1 run scoreboard players get @s rpg_ms_crossbow
data modify storage rpg:explore k.nx set value "都拿到了"
execute unless entity @s[tag=rpg.xm.5] run data modify storage rpg:explore k.nx set value "1200 点：传说图纸 ×1"
execute unless entity @s[tag=rpg.xm.4] run data modify storage rpg:explore k.nx set value "800 点：符文、符石、史诗图纸"
execute unless entity @s[tag=rpg.xm.3] run data modify storage rpg:explore k.nx set value "500 点：符石 ×1、货币 ×6"
execute unless entity @s[tag=rpg.xm.2] run data modify storage rpg:explore k.nx set value "300 点：史诗图纸 ×1"
execute unless entity @s[tag=rpg.xm.1] run data modify storage rpg:explore k.nx set value "150 点：符文 ×1、锻石 ×1"
execute unless entity @s[tag=rpg.xm.0] run data modify storage rpg:explore k.nx set value "50 点：图纸碎片 ×3、货币 ×3"
