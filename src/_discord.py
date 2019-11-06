async def e_send(ctx, embed=None, delay=None, message=None, **kwargs):
    """
    Clean messages with a delay
    """
    if embed is not None:
        await ctx.send(embed=embed, delete_after=delay)
    elif message is not None:
        await ctx.send(message, delete_after=delay)
    await ctx.message.delete()
