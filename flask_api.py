from io import BytesIO
from flask import Flask, request, send_file
from diffusers import StableDiffusionPipeline
from diffusers.schedulers.scheduling_utils import SchedulerMixin

from python_coreml_stable_diffusion.pipeline import CoreMLStableDiffusionPipeline
from python_coreml_stable_diffusion.coreml_model import (_load_mlpackage)

import logging
import gc

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__, static_url_path='', static_folder='frontend/build')

num_inference_steps = 20
model_version = "stabilityai/stable-diffusion-2-base"

def get_coreml_pipe(pytorch_pipe,
                    mlpackages_dir,
                    model_version,
                    compute_unit,
                    delete_original_pipe=True,
                    scheduler_override=None):
    """ Initializes and returns a `CoreMLStableDiffusionPipeline` from an original
    diffusers PyTorch pipeline
    """
    # Ensure `scheduler_override` object is of correct type if specified
    if scheduler_override is not None:
        assert isinstance(scheduler_override, SchedulerMixin)
        logger.warning(
            "Overriding scheduler in pipeline: "
            f"Default={pytorch_pipe.scheduler}, Override={scheduler_override}")

    # Gather configured tokenizer and scheduler attributes from the original pipe
    coreml_pipe_kwargs = {
        "tokenizer": pytorch_pipe.tokenizer,
        "scheduler": pytorch_pipe.scheduler if scheduler_override is None else scheduler_override,
        "feature_extractor": pytorch_pipe.feature_extractor,
    }

    model_names_to_load = ["text_encoder", "unet", "vae_decoder"]
    if getattr(pytorch_pipe, "safety_checker", None) is not None:
        model_names_to_load.append("safety_checker")
    else:
        logger.warning(
            f"Original diffusers pipeline for {model_version} does not have a safety_checker, "
            "Core ML pipeline will mirror this behavior.")
        coreml_pipe_kwargs["safety_checker"] = None

    if delete_original_pipe:
        del pytorch_pipe
        gc.collect()
        logger.info("Removed PyTorch pipe to reduce peak memory consumption")

    # Load Core ML models
    logger.info(f"Loading Core ML models in memory from {mlpackages_dir}")
    coreml_pipe_kwargs.update({
        model_name: _load_mlpackage(
            model_name,
            mlpackages_dir,
            model_version,
            compute_unit,
        )
        for model_name in model_names_to_load
    })
    logger.info("Done.")

    logger.info("Initializing Core ML pipe for image generation")
    coreml_pipe = CoreMLStableDiffusionPipeline(**coreml_pipe_kwargs)
    logger.info("Done.")

    return coreml_pipe

@app.route('/app/inference', methods=['POST'])
def handleAppInference():
    data = request.get_json()
    prompt = data["prompt"]
    pytorch_pipe = StableDiffusionPipeline.from_pretrained(model_version,
                                                           use_auth_token=True)
    coreml_pipe = get_coreml_pipe(pytorch_pipe=pytorch_pipe,
                                  mlpackages_dir="./models/coreml-stable-diffusion-2-base/original/packages",
                                  model_version=model_version,
                                  compute_unit="ALL",
                                  scheduler_override=None)
    image = coreml_pipe(
        prompt=prompt,
        height=coreml_pipe.height,
        width=coreml_pipe.width,
        num_inference_steps=num_inference_steps,
    )
    img_io = BytesIO()
    image["images"][0].save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')
    
if __name__ == "__main__":
    app.run(threaded=False, host='0.0.0.0', port=3000)