# 把自己当新人重走一遍（管理员）；旁白放到一半也从头来
execute if entity @s[tag=rpg.ob.intro] run function rpg:onboard/intro/stop
function rpg:onboard/admin/release
scoreboard players reset @s rpg_ident
scoreboard players reset @s rpg_ident_sin
scoreboard players reset @s rpg_messiah
scoreboard players reset @s rpg_pr_done
scoreboard players reset @s rpg_ob_v
# 力跟着身份走：重抽身份时一起重分（add_sephira.py）
scoreboard players reset @s rpg_force
tag @s remove rpg.fallen
tag @s remove rpg.ob.hold
tag @s remove rpg.ob.wait
tag @s remove rpg.ob.queued
function rpg:onboard/begin
