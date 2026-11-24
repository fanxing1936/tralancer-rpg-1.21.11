# 序章模式的血线（as/at 米迦勒，每 4 刻一次，由 #rpg:michael_boss/prologue_hp 调用）
execute unless score #state rpg_pr matches 7 run return 0
execute unless entity @s[tag=rpg.pr.hpset] run function rpg:prologue/michael/hp_set
scoreboard players operation #pct rpg_pr = @s rpg_mk_h
scoreboard players operation #pct rpg_pr *= #hund rpg_pr
scoreboard players operation #pct rpg_pr /= #mmax rpg_pr
execute if score #l2 rpg_pr matches 0 if score #pct rpg_pr matches ..75 run function rpg:prologue/michael/line2
execute if score #l3 rpg_pr matches 0 if score #pct rpg_pr matches ..50 run function rpg:prologue/michael/line3
execute if score #l4 rpg_pr matches 0 if score #pct rpg_pr matches ..35 run function rpg:prologue/michael/line4
execute if score #l1 rpg_pr matches 0 if score @s rpg_mk_sk matches 14..16 run function rpg:prologue/michael/line_l01
execute if score #pct rpg_pr matches ..25 run function rpg:prologue/michael/end
