async def e_send(ctx, delete, embed=None, delay=None, message=None):
    """
    Clean messages with a delay
    """
    if delete and delay is not None:
        if embed is not None:
            await ctx.send(embed=embed, delete_after=delay)
        elif message is not None:
            await ctx.send(message, delete_after=delay)
        await ctx.message.delete(delay=delay)
    else:
        if embed is not None:
            await ctx.send(embed=embed)
        elif message is not None:
            await ctx.send(message)

def convert_bool(arg):
    return 1 if arg.lower() in ('y', 'yes') else 0

def convert_str(arg):
    return 'Yes' if arg == 1 else 'No'