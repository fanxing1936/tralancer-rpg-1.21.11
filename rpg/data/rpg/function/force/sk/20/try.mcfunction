# 不死（as/at 施放者）
scoreboard players operation #lv rpg_fo = @s rpg_k20
execute unless score #lv rpg_fo matches 1.. run return run function rpg:force/fail/say {m:"还没学会不死"}
function rpg:force/fail/say {m:"不死是被动，学会就生效，不用放进槽里"}
