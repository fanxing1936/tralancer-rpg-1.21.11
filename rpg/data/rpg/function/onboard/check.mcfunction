# 新版本里第一次见到这名玩家（as 玩家）。用户 2026-11-23：所有人都要走一遍新手开局，老玩家也不例外。
# 已经在新手开局里抽过身份的人（这一版之前测试过的）算走完了，不再重来。
execute unless score @s rpg_fg_id matches 1.. run return 0
execute if score @s rpg_ident matches 1.. run scoreboard players set @s rpg_ob 100
execute if score @s rpg_ident matches 1.. run return run scoreboard players set @s rpg_ob_v 1
function rpg:onboard/begin
