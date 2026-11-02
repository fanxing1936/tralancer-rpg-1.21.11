# 拍摄环境：黄昏定格、晴天、不刷怪；玩家生存模式 + 无敌，这样路西法的招式会对准你。
gamerule advance_time false
gamerule advance_weather false
gamerule spawn_mobs false
gamerule spawn_phantoms false
gamerule show_death_messages false
time set 12600
weather clear
gamemode survival @s
function promo:god
tellraw @s {"text": "[宣传片] 拍摄环境就绪：黄昏、晴天、不刷怪。", "color": "#D9C9A3"}
