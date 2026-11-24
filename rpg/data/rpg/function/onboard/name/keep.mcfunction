execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id
function rpg:onboard/name/store with storage rpg:onboard tmp
function rpg:onboard/card/roll
# 起好名字直接去名字卡（序章入口从新手流程里拿掉了，用户 2026-11-23；玩家面板的「序章」按钮还在）
scoreboard players set @s rpg_ob 3
playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 0.8 0.8
function rpg:onboard/show
