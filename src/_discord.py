async def e_send(ctx, embed=None, delay=None):
    """Clean messages with a delay"""
    await ctx.send(embed=embed, delete_after=delay)
    await ctx.message.delete(delay=delay)
