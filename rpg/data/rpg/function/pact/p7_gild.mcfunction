# 一堆掉落物翻一倍。读出这堆的数量、翻倍、写回去 —— 比逐件复制便宜得多。
# 只处理 32 及以下的堆：再多翻倍就越过 64 的堆叠上限了。
particle wax_on ~ ~0.4 ~ 0.2 0.2 0.2 0.05 8
execute store result score #gild rpg_pact run data get entity @s Item.count
execute if score #gild rpg_pact matches 1..32 run function rpg:pact/p7_double
