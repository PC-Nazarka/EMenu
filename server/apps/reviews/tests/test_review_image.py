import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.reviews.factories import ReviewFactory, ReviewImageFactory
from apps.reviews.models import Review, ReviewImage

pytestmark = pytest.mark.django_db

COUNT_IMAGES = 2


def test_create_review_images_by_manager(
    manager,
    api_client,
) -> None:
    review = ReviewFactory.create()
    review_images = ReviewImageFactory.build_batch(size=COUNT_IMAGES)
    data = {
        "images": [image.image for image in review_images],
        "review": review.pk,
    }
    api_client.force_authenticate(user=manager.user)
    response = api_client.post(
        reverse_lazy(
            "api:reviews-images",
            kwargs={"pk": review.pk}
        ),
        data=data,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_review_images_by_manager(
    manager,
    api_client,
) -> None:
    review = ReviewFactory.create()
    review_images = ReviewImageFactory.create_batch(
        size=COUNT_IMAGES,
        review=review,
    )
    ids = [image.id for image in review_images]
    api_client.force_authenticate(user=manager.user)
    for image in review_images:
        api_client.delete(
            reverse_lazy(
                "api:review-images-detail",
                kwargs={"pk": image.pk},
            ),
        )
    assert not ReviewImage.objects.filter(id__in=ids).exists()
    assert not Review.objects.get(id=review.id).images.all().exists()


def test_create_review_images_by_client(
    client,
    api_client,
) -> None:
    review = ReviewFactory.create(client=client)
    review_images = ReviewImageFactory.build_batch(size=COUNT_IMAGES)
    data = {
        "images": [image.image for image in review_images],
        "review": review.id,
    }
    api_client.force_authenticate(user=client.user)
    response = api_client.post(
        reverse_lazy(
            "api:reviews-images",
            kwargs={"pk": review.pk}
        ),
        data=data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Review.objects.get(id=review.id).images.count() == COUNT_IMAGES
    assert Review.objects.get(id=review.id).images.all().exists()


def test_delete_review_images_by_client(
    client,
    api_client,
) -> None:
    review = ReviewFactory.create(client=client)
    review_images = ReviewImageFactory.create_batch(
        size=COUNT_IMAGES,
        review=review,
    )
    api_client.force_authenticate(user=client.user)
    for image in review_images:
        api_client.delete(
            reverse_lazy(
                "api:review-images-detail",
                kwargs={"pk": image.pk},
            ),
        )
    assert not ReviewImage.objects.filter(
        id__in=[image.id for image in review_images]
    ).exists()
    assert not Review.objects.get(id=review.id).images.all().exists()


def test_delete_review_images_other_client_by_client(
    client,
    api_client,
) -> None:
    review = ReviewFactory.create()
    review_images = ReviewImageFactory.create_batch(
        size=COUNT_IMAGES,
        review=review,
    )
    api_client.force_authenticate(user=client.user)
    for image in review_images:
        api_client.delete(
            reverse_lazy(
                "api:review-images-detail",
                kwargs={"pk": image.pk},
            ),
        )
    assert ReviewImage.objects.filter(
        id__in=[image.id for image in review_images]
    ).exists()
    assert Review.objects.get(id=review.id).images.exists()


def test_create_review_images_by_not_auth(
    api_client,
) -> None:
    review = ReviewFactory.create()
    review_images = ReviewImageFactory.build_batch(size=COUNT_IMAGES)
    data = {
        "images": [image.image for image in review_images],
        "review": review.id,
    }
    response = api_client.post(
        reverse_lazy(
            "api:reviews-images",
            kwargs={"pk": review.pk}
        ),
        data=data,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_review_images_by_not_auth(
    api_client,
) -> None:
    review = ReviewFactory.create()
    review_images = ReviewImageFactory.create_batch(
        size=COUNT_IMAGES,
        review=review,
    )
    for image in review_images:
        api_client.delete(
            reverse_lazy(
                "api:dish-images-detail",
                kwargs={"pk": image.pk},
            ),
        )
    assert ReviewImage.objects.filter(
        id__in=[image.id for image in review_images]
    ).exists()
    assert Review.objects.get(id=review.id).images.all().exists()