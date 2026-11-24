execute if entity @a[tag=rpg.fo.me,limit=1,scores={rpg_ident=4,rpg_ident_sin=2}] run function rpg:force/x/id/envy
execute if entity @a[tag=rpg.fo.me,limit=1,scores={rpg_ident=4,rpg_ident_sin=6}] run function rpg:force/x/id/lust
execute if entity @a[tag=rpg.fo.me,limit=1,scores={rpg_ident=5}] run function rpg:force/x/id/son
execute if entity @a[tag=rpg.fo.me,limit=1,scores={rpg_pillar=1,rpg_sef=6..}] run function rpg:force/x/id/vsboss
execute unless score #pct rpg_fo matches 1.. run return 0
scoreboard players operation #dmg rpg_fo = #dd rpg_fo
scoreboard players operation #dmg rpg_fo *= #pct rpg_fo
scoreboard players operation #dmg rpg_fo /= #100 rpg_fo
execute unless score #dmg rpg_fo matches 1.. run return 0
execute store result storage rpg:force h.d float 0.1 run scoreboard players get #dmg rpg_fo
function rpg:force/hit_no with storage rpg:force h
