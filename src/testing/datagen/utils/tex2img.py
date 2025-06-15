import matplotlib.pyplot as plt

def tex2img(texData: str, outFileName: str, extension='png', dpi=600, fontsize=12) -> int:
  err = 0
  fileName = f'{outFileName}.{extension}'
  
  plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": fontsize,
    "text.latex.preamble": r"""
            \usepackage{amsmath}
            \usepackage{amsfonts}
            \usepackage{amssymb}
        """
  })
  
  fig = plt.figure(figsize=(0.2, 0.2), facecolor="none", dpi=dpi)
  ax = fig.add_axes([0, 0, 1, 1], frameon=False)
  ax.axis("off")

  try:
    ax.text(
       0.5, 0.5, 
       f"${texData}$", 
       ha="center", 
       va="center", 
       transform=ax.transAxes
    )

    plt.savefig(
        f"{fileName}",
        format=extension,
        transparent=True,
        bbox_inches="tight",
        pad_inches=0,
        dpi=dpi,
    )
  
  except Exception as e:
    print(f"Ошибка при рендеринге формулы: {e}")
    err = 1
  finally:
    plt.close()
    return err
