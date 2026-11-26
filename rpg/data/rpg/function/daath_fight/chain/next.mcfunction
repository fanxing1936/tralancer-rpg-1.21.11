execute unless score @s rpg_dt_cl matches 1.. run return run function rpg:daath_fight/chain/done
scoreboard players remove @s rpg_dt_cl 1
execute if entity @a[tag=rpg.dt.me,distance=..9] run function rpg:daath_fight/weapon/pick_melee
execute unless entity @a[tag=rpg.dt.me,distance=..9] run return run function rpg:daath_fight/chain/done
scoreboard players set @s rpg_dt_t 0
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute if score @s rpg_dt_wc matches 0 run function rpg:daath_fight/hit/c_fist
execute if score @s rpg_dt_wc matches 1 run function rpg:daath_fight/hit/c_sword
execute if score @s rpg_dt_wc matches 2 run function rpg:daath_fight/hit/c_axe
execute if score @s rpg_dt_wc matches 3 run function rpg:daath_fight/hit/c_mace
execute if score @s rpg_dt_wc matches 4 run function rpg:daath_fight/hit/c_spear
execute if score @s rpg_dt_wc matches 5 run function rpg:daath_fight/hit/c_glaive
execute if score @s rpg_dt_wc matches 6 run function rpg:daath_fight/hit/c_dagger
execute if score @s rpg_dt_wc matches 7 run function rpg:daath_fight/hit/c_scythe
